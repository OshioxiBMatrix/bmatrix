from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart, CartItem
from shop.models import Product

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    items = cart.items.all()
    return render(request, 'cart/view_cart.html', {'cart': cart, 'items': items})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity += 1
    item.save()
    return redirect('cart:view_cart')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart:view_cart')
