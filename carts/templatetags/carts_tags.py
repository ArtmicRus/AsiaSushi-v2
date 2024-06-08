from django import template

from carts.utils import get_user_cart, get_user_cart_items


register = template.Library()

@register.simple_tag()
def user_cart_items(request):
    return get_user_cart_items(request)

@register.simple_tag()
def user_cart(cart_items):
    return get_user_cart(cart_items)