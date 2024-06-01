from carts.models import CartItem


def get_user_carts(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user).select_related('product').order_by('product')
    
    if not request.session.session_key:
        request.session.create()
    return CartItem.objects.filter(session_key=request.session.session_key).select_related('product')