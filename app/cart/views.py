from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Cart, CartItem
from shop.models import Product

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

def cart_detail(request):
    """View to display the cart contents"""
    cart = _get_or_create_cart(request)
    cart_items = cart.items.all().select_related('product')
    
    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
    }
    
    return render(request, 'cart/cart_detail.html', context)

def add_to_cart(request, product_id):
    """View to add a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    cart = _get_or_create_cart(request)
    
    # Check if product is already in cart
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        # Update quantity
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Đã cập nhật số lượng {product.name} trong giỏ hàng.')
    except CartItem.DoesNotExist:
        # Add new item
        quantity = int(request.POST.get('quantity', 1))
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        messages.success(request, f'Đã thêm {product.name} vào giỏ hàng.')
    
    # If AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_count = cart.items.count()
        return JsonResponse({
            'success': True,
            'message': f'Đã thêm {product.name} vào giỏ hàng.',
            'cart_count': cart_count
        })
    
    # Redirect back to the product page or to cart
    next_url = request.POST.get('next', '')
    if next_url:
        return redirect(next_url)
    else:
        return redirect('shop:product_detail', slug=product.slug)

def remove_from_cart(request, item_id):
    """View to remove an item from the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    product_name = cart_item.product.name
    
    # Check if the cart belongs to the current user/session
    cart = _get_or_create_cart(request)
    if cart_item.cart.id == cart.id:
        cart_item.delete()
        messages.success(request, f'Đã xóa {product_name} khỏi giỏ hàng.')
    
    # If AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_count = cart.items.count()
        cart_items = cart.items.all().select_related('product')
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'message': f'Đã xóa {product_name} khỏi giỏ hàng.',
            'cart_count': cart_count,
            'total': float(total)
        })
    
    return redirect('cart:cart_detail')

def update_cart(request, item_id):
    """View to update the quantity of an item in the cart"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Check if the cart belongs to the current user/session
    cart = _get_or_create_cart(request)
    if cart_item.cart.id == cart.id:
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Đã cập nhật giỏ hàng.')
            else:
                cart_item.delete()
                messages.success(request, f'Đã xóa {cart_item.product.name} khỏi giỏ hàng.')
        except ValueError:
            messages.error(request, 'Số lượng không hợp lệ.')
    
    # If AJAX request, return JSON response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        cart_items = cart.items.all().select_related('product')
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        return JsonResponse({
            'success': True,
            'item_total': float(cart_item.product.price * cart_item.quantity) if cart_item.id else 0,
            'total': float(total)
        })
    
    return redirect('cart:cart_detail')
