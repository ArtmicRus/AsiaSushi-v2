from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render

from promotions.models import Promotion


def index(request):

    context = {
        'title': 'Asia - Главная страница',
        'content': 'Азия суши - Продажа суши и пиццы!',
        "year": datetime.now().year,
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Asia - О нас',
        'content': 'О нас',
        "year": datetime.now().year,
    }

    return render(request, 'main/about.html', context)

def contact(request):
    context = {
        'title': 'Asia - Контактная информация',
        'content': 'Контакты',
        "year": datetime.now().year,
    }

    return render(request, 'main/contact.html', context)
