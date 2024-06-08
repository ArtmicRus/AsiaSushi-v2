from django import template

from promotions.utils import get_user_promotion_items_by_cart_id


register = template.Library()

# @register.filter
# def user_promotion_items(request):
#     return get_user_promotion_items_by_cart_id(request)