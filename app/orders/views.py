from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .models import Order, OrderItem, VNPayTransaction
from cart.models import Cart, CartItem
from shop.models import Product

import hashlib
import hmac
import urllib.parse
import datetime
import random
import requests

# VNPay configuration
VNPAY_TMN_CODE = "KSN80HXK"
VNPAY_HASH_SECRET = "1P6V7SEW6FV36UUB0TSCQL35JXZ6JSJ1"
VNPAY_PAYMENT_URL = "https://sandbox.vnpayment.vn/paymentv2/vpcpay.html"
VNPAY_RETURN_URL = "payment/vnpay_return"
VNPAY_API_URL = "https://sandbox.vnpayment.vn/merchant_webapi/api/transaction"

# Vietnamese address API
PROVINCE_API_URL = "https://provinces.open-api.vn/api/p/"
DISTRICT_API_URL = "https://provinces.open-api.vn/api/p/{}/d/"
WARD_API_URL = "https://provinces.open-api.vn/api/d/{}/w/"

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_provinces():
    """Get list of provinces from API"""
    try:
        response = requests.get(PROVINCE_API_URL)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching provinces: {e}")
        return []

def get_districts(province_id):
    """Get list of districts for a province from API"""
    try:
        response = requests.get(DISTRICT_API_URL.format(province_id))
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching districts: {e}")
        return []

def get_wards(district_id):
    """Get list of wards for a district from API"""
    try:
        response = requests.get(WARD_API_URL.format(district_id))
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error fetching wards: {e}")
        return []

def _get_or_create_cart(request):
    """Helper function to get or create a cart for the current session/user"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                cart = Cart.objects.create()
                request.session['cart_id'] = cart.id
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    
    return cart

@login_required
def checkout(request):
    """View for checkout page"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all().select_related('product')
    
    if not cart_items:
        messages.warning(request, 'Giỏ hàng của bạn đang trống.')
        return redirect('cart:cart_detail')
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)
    shipping_fee = 0  # Can be calculated based on location or weight
    
    # Get provinces for address form
    provinces = get_provinces()
    
    # Get user info if available
    user = request.user
    initial_data = {}
    if user.is_authenticated:
        initial_data = {
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'email': user.email,
        }
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'shipping_fee': shipping_fee,
        'grand_total': total + shipping_fee,
        'provinces': provinces,
        'initial_data': initial_data
    }
    
    return render(request, 'orders/checkout.html', context)

@login_required
@transaction.atomic
def place_order(request):
    """Process the order form and create a new order"""
    if request.method != 'POST':
        return redirect('orders:checkout')
    
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all().select_related('product')
    
    if not cart_items:
        messages.warning(request, 'Giỏ hàng của bạn đang trống.')
        return redirect('cart:cart_detail')
    
    # Get form data
    full_name = request.POST.get('full_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    province = request.POST.get('province')
    district = request.POST.get('district')
    ward = request.POST.get('ward')
    address = request.POST.get('address')
    payment_method = request.POST.get('payment_method')
    note = request.POST.get('note', '')
    
    # Validate required fields
    if not all([full_name, email, phone, province, district, ward, address, payment_method]):
        messages.error(request, 'Vui lòng điền đầy đủ thông tin.')
        return redirect('orders:checkout')
    
    # Calculate totals
    items_total = sum(item.product.price * item.quantity for item in cart_items)
    shipping_fee = 0  # Can be calculated based on location or weight
    
    # Create order
    order = Order.objects.create(
        user=request.user,
        full_name=full_name,
        email=email,
        phone=phone,
        province=province,
        district=district,
        ward=ward,
        address=address,
        payment_method=payment_method,
        shipping_fee=shipping_fee,
        note=note,
        status='pending',
        paid=(payment_method != 'cod')  # Mark as paid only for non-COD orders
    )
    
    # Create order items
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            price=cart_item.product.price,
            quantity=cart_item.quantity
        )
        
        # Update product stock
        product = cart_item.product
        product.stock -= cart_item.quantity
        product.save()
    
    # Clear the cart
    cart_items.delete()
    
    # Process payment based on method
    if payment_method == 'vnpay':
        return redirect('orders:vnpay_payment', order_id=order.id)
    else:
        # For COD, go directly to order complete page
        messages.success(request, 'Đặt hàng thành công! Cảm ơn bạn đã mua hàng.')
        return redirect('orders:order_complete', order_id=order.id)

@login_required
def order_complete(request, order_id):
    """Display order completion page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    
    return render(request, 'orders/order_complete.html', context)

@login_required
def vnpay_payment(request, order_id):
    """Create a VNPay payment URL and redirect user to VNPay"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.paid:
        messages.info(request, 'Đơn hàng này đã được thanh toán.')
        return redirect('orders:order_complete', order_id=order.id)
    
    # Create a unique transaction reference
    txn_ref = f"{order.id}-{int(datetime.datetime.now().timestamp())}-{random.randint(1000, 9999)}"
    
    # Create VNPay transaction record
    transaction = VNPayTransaction.objects.create(
        order=order,
        amount=order.get_total_cost(),
        vnp_txn_ref=txn_ref,
        status='pending'
    )
    
    # Prepare VNPay parameters
    vnp_params = {
        "vnp_Version": "2.1.0",
        "vnp_Command": "pay",
        "vnp_TmnCode": VNPAY_TMN_CODE,
        "vnp_Amount": int(order.get_total_cost() * 100),  # Amount in VND, multiply by 100 (no decimal)
        "vnp_CurrCode": "VND",
        "vnp_TxnRef": txn_ref,
        "vnp_OrderInfo": f"Thanh toan don hang {order.id} tai BMATRIX",
        "vnp_OrderType": "other",
        "vnp_Locale": "vn",
        "vnp_ReturnUrl": request.build_absolute_uri(reverse('orders:vnpay_callback')),
        "vnp_IpAddr": get_client_ip(request),
        "vnp_CreateDate": datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
    }
    
    # Sort parameters by key
    sorted_params = sorted(vnp_params.items(), key=lambda x: x[0])
    hash_data = "&".join([f"{k}={v}" for k, v in sorted_params])
    
    # Create signature
    hmac_obj = hmac.new(VNPAY_HASH_SECRET.encode('utf-8'), hash_data.encode('utf-8'), hashlib.sha512)
    vnp_params["vnp_SecureHash"] = hmac_obj.hexdigest()
    
    # Create payment URL
    payment_url = VNPAY_PAYMENT_URL + "?" + urllib.parse.urlencode(vnp_params)
    
    return redirect(payment_url)

@csrf_exempt
def vnpay_callback(request):
    """Handle VNPay payment callback"""
    if request.method != 'GET':
        return HttpResponse("Invalid request method", status=400)
    
    # Get all parameters
    params = request.GET.dict()
    
    # Extract secure hash from params
    vnp_secure_hash = params.pop('vnp_SecureHash', '')
    
    # Sort parameters by key
    sorted_params = sorted(params.items(), key=lambda x: x[0])
    hash_data = "&".join([f"{k}={v}" for k, v in sorted_params])
    
    # Verify signature
    hmac_obj = hmac.new(VNPAY_HASH_SECRET.encode('utf-8'), hash_data.encode('utf-8'), hashlib.sha512)
    calculated_hash = hmac_obj.hexdigest()
    
    # Get transaction reference and response code
    vnp_txn_ref = params.get('vnp_TxnRef', '')
    vnp_response_code = params.get('vnp_ResponseCode', '')
    
    try:
        # Find the transaction
        transaction = VNPayTransaction.objects.get(vnp_txn_ref=vnp_txn_ref)
        order = transaction.order
        
        # Update transaction with response data
        transaction.vnp_response_code = vnp_response_code
        transaction.vnp_bank_code = params.get('vnp_BankCode', '')
        transaction.vnp_bank_tran_no = params.get('vnp_BankTranNo', '')
        transaction.vnp_card_type = params.get('vnp_CardType', '')
        transaction.vnp_transaction_no = params.get('vnp_TransactionNo', '')
        
        # Check if payment is successful
        if vnp_secure_hash == calculated_hash and vnp_response_code == '00':
            transaction.status = 'completed'
            order.paid = True
            order.payment_id = vnp_txn_ref
            order.save()
            transaction.save()
            
            messages.success(request, 'Thanh toán thành công! Cảm ơn bạn đã mua hàng.')
            return redirect('orders:order_complete', order_id=order.id)
        else:
            transaction.status = 'failed'
            transaction.save()
            
            messages.error(request, 'Thanh toán thất bại. Vui lòng thử lại hoặc chọn phương thức thanh toán khác.')
            return redirect('orders:checkout')
            
    except VNPayTransaction.DoesNotExist:
        messages.error(request, 'Không tìm thấy giao dịch. Vui lòng liên hệ với chúng tôi để được hỗ trợ.')
        return redirect('orders:checkout')

@login_required
def my_orders(request):
    """Display user's orders"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    
    return render(request, 'orders/my_orders.html', context)

@login_required
def order_detail(request, order_id):
    """Display order details"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'order_items': order.items.all()
    }
    
    return render(request, 'orders/order_detail.html', context)

# API endpoints for address selection
def get_districts_api(request, province_id):
    """API endpoint to get districts for a province"""
    districts = get_districts(province_id)
    return JsonResponse(districts, safe=False)

def get_wards_api(request, district_id):
    """API endpoint to get wards for a district"""
    wards = get_wards(district_id)
    return JsonResponse(wards, safe=False)
