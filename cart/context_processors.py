from .cart import Cart

def cart_context(request):
    """Make cart available globally in templates."""
    cart = Cart(request)
    return {'cart_count': len(cart)}


# from .cart import Cart

# def cart_context(request):
#     cart = Cart(request)
#     return {'cart': cart}
