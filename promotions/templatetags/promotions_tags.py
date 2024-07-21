from django import template

from promotions.utils import get_user_promotion_items_by_cart_id


register = template.Library()

@register.simple_tag()
def user_promotion_items(request, cart_items):
    return get_user_promotion_items_by_cart_id(request, cart_items)