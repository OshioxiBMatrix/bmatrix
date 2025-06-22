from django.shortcuts import render, redirect
from .models import Order, OrderItem
from cart.models import Cart, CartItem

def create_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    order = Order.objects.create(
        user=request.user,
        address="Địa chỉ demo",
        phone="SĐT demo",
        paid=False
    )
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )
    cart.items.all().delete()
    return redirect('orders:order_history')

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})
