from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from carts.utils import get_user_cart_items
from promotions.models import Promotion, PromotionProducts
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

def promotion_add_to_cart(request):
    
    promotion_id = request.POST.get("promotion_id")
    promotion = Promotion.objects.get(id=promotion_id)

    if request.user.is_authenticated:
        try:
            user_carts= get_user_cart_items(request)

            if user_carts:
                cart = user_carts.first().cart

            carts = Cart.objects.filter(id=user_carts.first().cart.pk)

            if carts.exists():
                cart = carts.first()

                if promotion.promotion_terms.is_need_min_price:
                    user_carts_sum = user_carts.total_price()

                    if user_carts_sum >= promotion.promotion_terms.min_price:
                        
                        cart.promotion = promotion
                        cart.save()
                    else:
                        response_data = {
                            "message": f"В вашей корзине не хватает {promotion.promotion_terms.min_price - user_carts_sum} Руб. для добавления этой акции",
                        }
                        return JsonResponse(response_data, status=400)

        except Exception:
            response_data = {
                "message": "Вы не можете добавить акцию в пустую корзину",
            }

            return JsonResponse(response_data, status=400)
        
    else:
        response_data = {
                "message": "Добавление акций в корзину невозможно для неавторизованных пользователей",
            }
        
        return JsonResponse(response_data, status=401)
    
    user_cart= get_user_cart_items(request)
    promotion_products = PromotionProducts.objects.filter(promotion=promotion)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"cart_items": user_cart,
         "promotion_products":promotion_products}, 
         request=request
    )

    response_data ={
        "message": "Акция добавлена в корзину",
        "cart_with_promotion_html": cart_items_html,
    }

    return JsonResponse(response_data)


def promotion_delete_from_cart(request):

    cart_id = request.POST.get("cart_id")

    cart = Cart.objects.get(id=cart_id)
    cart.promotion = None

    user_cart = get_user_cart_items(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"cart_items": user_cart}, 
        request=request
    )

    # Структура Json
    response_data = {
        "message": "Акция удалена из корзины",
        "cart_items_html": cart_items_html
    }

    return JsonResponse(response_data)