from carts.models import Cart, CartItem


def get_user_cart_items(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        if cart.exists():
            cart = cart.first()
            return CartItem.objects.filter(cart=cart).select_related('product').order_by('product')
    
    if not request.session.session_key:
        request.session.create()
    return CartItem.objects.filter(session_key=request.session.session_key).select_related('product')

def get_user_cart(cart_items):
    
    if cart_items:
        cart_item = cart_items.first()
        cart = Cart.objects.filter(id=cart_item.cart.pk)
        return cart