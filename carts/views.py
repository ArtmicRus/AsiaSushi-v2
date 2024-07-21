from django.http import JsonResponse
from django.template.loader import render_to_string

from carts.models import Cart, CartItem
from carts.utils import get_user_cart_items
from goods.models import Products
from promotions.models import PromotionProducts


def cart_add(request):
    """Добавление товара в корзину"""
    product_id = request.POST.get("product_id")

    product = Products.objects.get(id=product_id)

    cart = None

    # Надстройка Корзина для объединение Акций и Товаров в корзине
    if request.user.is_authenticated:

        cart = Cart.objects.filter(user=request.user)

        if cart.exists():
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.create(user=request.user)


        # Берём определённый товар в корзине
        cart_items = CartItem.objects.filter(cart=cart, product=product)

        # Если хоть что то нашли то берём его как объект в переменную cart_item
        if cart_items.exists():
            cart_item = cart_items.first()

            # Проверяем найден ли объект или нет и если найден то добавляем
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
        # Если ничего не нашли создаём новый элемент корзины
        else:
            CartItem.objects.create(cart=cart, product=product, quantity=1)

    else:

        # Находим содержимое строки-корзины
        cart_items = CartItem.objects.filter(
            session_key=request.session.session_key,
            product=product
            )
            
        # Проверяем найден ли объект или нет и если найден то добавляем
        if cart_items.exists():
            cart_item = cart_items.first()
            if cart_item:
                cart_item.quantity += 1
                cart_item.save()
                cart = cart_item.cart
        else:
            cart_items = CartItem.objects.filter(session_key=request.session.session_key)
            
            if cart_items.exists():
                cart = cart_items.first().cart
            else:
                cart = Cart.objects.create()

            CartItem.objects.create(
                cart=cart,
                session_key=request.session.session_key, 
                product=product, 
                quantity=1
            )
    

    # Берём акционные предметы
    if cart.promotion:
        promotion_products = PromotionProducts.objects.filter(promotion = cart.promotion)
    else:
        promotion_products = None

    user_cart_items= get_user_cart_items(request)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"cart_items": user_cart_items,
         "promotion_products": promotion_products},
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
    cart_item_id = request.POST.get("cart_id")
    quantity = request.POST.get("quantity")

    cart_item = CartItem.objects.get(id=cart_item_id)

    cart_item.quantity = quantity
    cart_item.save()

    # Корзина с акциями (если есть)
    cart = cart_item.get_cart()

    if cart.promotion:
        promotion_products = PromotionProducts.objects.filter(promotion = cart.promotion)
    else:
        promotion_products = None

    cart_item = get_user_cart_items(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"cart_items": cart_item,
         "promotion_products": promotion_products}, 
        request=request
    )

    response_data = {
        "message": "Количество изменено",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response_data)

def cart_remove(request):
    
    cart_item_id = request.POST.get("cart_id")

    cart_item = CartItem.objects.get(id=cart_item_id)
    quantity = cart_item.quantity
    cart_item.delete()

    # Карзина с акциями (если есть)
    cart = cart_item.get_cart()

    if cart.promotion:
        promotion_products = PromotionProducts.objects.filter(promotion = cart.promotion)
    else:
        promotion_products = None

    user_cart = get_user_cart_items(request)
    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", 
        {"cart_items": user_cart,
         "promotion_products": promotion_products}, 
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
