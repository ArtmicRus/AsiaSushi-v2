from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from carts.utils import get_user_carts
from promotions.models import Promotion
from carts.models import Cart

# Create your views here.
def promotions(request):

    promo = Promotion.objects.all()

    context = {
        'promotions': promo,
        'title': 'Asia - Акции',
        "year": datetime.now().year,
    }

    return render(request, 'promotions/promotions.html', context)

def promotions_add_to_cart(request):
    
    promotion_id = request.POST.get("promotion_id")
    promotion = Promotion.objects.get(id=promotion_id)

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        user_carts= get_user_carts(request)

        if cart.exists():
            if promotion.promotion_terms.is_need_min_price:
                user_carts_sum = user_carts.total_price

                if user_carts_sum >= promotion.promotion_terms.min_price:
                    
                    cart.promotion = promotion
                    cart.save()
    else:
        response_data ={
                "message": "Добавление акций в корзину невозможно для неавторизованных пользователей",
            }
    
    user_cart= get_user_carts(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"carts": user_cart}, 
        request=request
    )

    response_data ={
        "message": "Товар добавлен в корзину",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)


def promotions_delete_from_cart(request):

    promo = Promotion.objects.all()

    context = {
        'promotions': promo,
        'title': 'Asia - Акции',
        "year": datetime.now().year,
    }

    return render(request, 'promotions/promotions.html', context)