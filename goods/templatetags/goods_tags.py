from django import template

from goods.models import Categories

register = template.Library()

# Тэг который можно ВЫЗВАТЬ В РАЗМЕТКЕ
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()