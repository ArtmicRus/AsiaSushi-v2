from promotions.models import Promotion, PromotionProducts


def get_user_promotion_items_by_cart_id(request, cart_items):
    if request.user.is_authenticated:
        if cart_items:
            cart = cart_items.first().cart
            if cart.promotion:
                promo = Promotion.objects.filter(id=cart.promotion.id).first()
                if promo:
                    return PromotionProducts.objects.filter(promotion_id=promo.pk)