
from django import template
from django.utils.http import urlencode

from goods.models import Categories

register = template.Library()

# Тэг который можно ВЫЗВАТЬ В РАЗМЕТКЕ
# А конкретно этот тэг для того чтобы вызвать список категорий
@register.simple_tag()
def tag_categories():
    return Categories.objects.all()

# Тэг с параметром 
# takes_context=True значит что все контекстные переменные будут доступны через параметры контепкста
# (Попадут в context)
#
@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    # Мы берём из переменной контекста request и берём от туда данные в виде словаря
    query=context['request'].GET.dict()
    # Расширение кваргсом????
    query.update(kwargs)
    # urlencode Формирует строку которую можно использовать как URL запрос
    return urlencode(query)