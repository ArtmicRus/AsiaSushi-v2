from promotions.models import Promotion


def get_user_promotion_items_by_cart_id(request, cart):
    if request.user.is_authenticated:
        return Promotion.objects.filter(cart=cart).select_related('cart').select_related('promotion')