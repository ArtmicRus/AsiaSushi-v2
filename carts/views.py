from django.http import JsonResponse
from django.template.loader import render_to_string

from carts.models import CartItem
from carts.utils import get_user_carts
from goods.models import Products


def cart_add(request):
    """Добавление товара в корзину"""
    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = CartItem.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            CartItem.objects.create(user=request.user, product=product, quantity=1)
    else:
        carts = CartItem.objects.filter(
            session_key=request.session.session_key, 
            product=product
            )
            

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            CartItem.objects.create(
                session_key=request.session.session_key, 
                product=product, 
                quantity=1
            )
    
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

    # Переадресация на страницу откуда мы вызвали данный контроллер
    #return redirect(request.META['HTTP_REFERER'])

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart = CartItem.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"carts": cart}, 
        request=request
    )

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)

def cart_remove(request):
    
    cart_id = request.POST.get("cart_id")

    cart = CartItem.objects.get(id=cart_id)
    quantity = cart.quantity
    cart.delete()

    user_cart = get_user_carts(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"carts": user_cart}, 
        request=request
    )

    # Структура Json
    response_data = {
        "message": "Товар удалён",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity,
    }

    return JsonResponse(response_data)
    
    # Переадресация на страницу откуда мы вызвали данный контроллер
    #return redirect(request.META['HTTP_REFERER'])
