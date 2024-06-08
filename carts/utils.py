from carts.models import Cart, CartItem


def get_user_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user).select_related('product').order_by('product')
    
    if not request.session.session_key:
        request.session.create()
    return CartItem.objects.filter(session_key=request.session.session_key).select_related('product')

def get_user_cart(cart_items):
    
    cart_item = cart_items.first()
    cart = Cart.objects.filter(id=cart_item.cart.pk)
    return cart