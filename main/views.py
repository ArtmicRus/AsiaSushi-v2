from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories

def index(request):

    context = {
        'title': 'AsiaSushi - Главная',
        'content': 'Азия суши - Продажа суши и пиццы!'
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'AsiaSushi - О нас',
        'content': 'О нас',
        'text_on_page': 'Тестовый текст о том почему у нас самые вкусные суши и пицца!!!'
    }

    return render(request, 'main/about.html', context)
