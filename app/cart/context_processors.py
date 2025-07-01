from .models import Cart, CartItem

def cart_context(request):
    """
    Context processor to provide cart information to all templates
    """
    cart_count = 0
    cart_total = 0
    
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)
            cart_count = cart_items.count()
            cart_total = sum(item.product.price * item.quantity for item in cart_items)
        except Cart.DoesNotExist:
            pass
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            try:
                cart = Cart.objects.get(id=cart_id)
                cart_items = CartItem.objects.filter(cart=cart)
                cart_count = cart_items.count()
                cart_total = sum(item.product.price * item.quantity for item in cart_items)
            except Cart.DoesNotExist:
                pass
    
    return {
        'cart_count': cart_count,
        'cart_total': cart_total,
    } 