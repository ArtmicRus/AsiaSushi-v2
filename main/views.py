from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

from goods.models import Categories

def index(request):

    context = {
        'title': 'Азия суши - Главная',
        'content': 'Азия суши - Продажа суши и пиццы!',
        "year": datetime.now().year,
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Азия суши - О нас',
        'content': 'О нас',
        "year": datetime.now().year,
        'text_on_page': 'Тестовый текст о том почему у нас самые вкусные суши и пицца!!!',
    }

    return render(request, 'main/about.html', context)

def contact(request):
    context = {
        'title': 'Азия суши- Контактная информация',
        'content': 'Контакты',
        "year": datetime.now().year,
    }

    return render(request, 'main/contact.html', context)
