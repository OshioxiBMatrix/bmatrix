def cart(request):
    """
    Context processor to make cart data available to all templates
    """
    return {
        'cart': getattr(request, 'cart', None),
        'cart_item_count': 0,  # Default value, will be updated when cart functionality is implemented
        'cart_total': 0  # Default value, will be updated when cart functionality is implemented
    } 