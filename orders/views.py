from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.models import Cart, CartItem
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem, OrderStatus
from orders.utils import create_statuses
from promotions.models import PromotionProducts

@login_required 
def create_order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                # Атомарная транзакция - вкратце это Транзакция как она есть
                # То есть всё что ниже должно быть сделано или откат всего
                with transaction.atomic():
                    user = request.user
                    cart = Cart.objects.filter(user=user).first()

                    cart_items = CartItem.objects.filter(cart=cart)

                    if cart_items.exists():
                        # Проверяем есть ли стутусы
                        start_status = OrderStatus.objects.filter(name='В обработке')
                        if not start_status: # если статусов нет то создаём
                            create_statuses()

                        # Есть к корзине добавена Акция ищем акционные товар выбранный при заказе
                        if cart.promotion:
                            promotion_item = PromotionProducts.objects.filter(
                                id=form.cleaned_data['promotion_item_id']
                                ).first()

                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                            order_status_id=1,
                        )
                        # Создать заказанные основные товары
                        for cart_item in cart_items:
                            product=cart_item.product
                            name=cart_item.product.name
                            price=cart_item.product.self_price()
                            quantity=cart_item.quantity

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                        # Создаём тавар заказа из акционного если есть акция
                        if cart.promotion:
                            OrderItem.objects.create(
                                    order=order,
                                    product=promotion_item.product,
                                    name=promotion_item.product.name,
                                    price=0,
                                    quantity=1,
                                )

                        # Очистить корзину пользователя после создания заказа
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')
                        return redirect('user:profile')
            except ValidationError as e:
                messages.success(request, str(e))
                return redirect('cart:order')
    else:
        initial = {
            'first_name': request.user.first_name,
            'phone_number': request.user.phone_number,
            }

        # initial = изначальные данные куда мы передаём предзаполненные данные
        # для авторизованных пользователей
        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Asia - Оформление заказа',
        'form': form,
        'order': True,
    }
    return render(request, 'orders/create_order.html', context=context)


@login_required 
def delete_order(request, order_id):
    Order.objects.get(id=order_id).delete()
    return redirect(request.META['HTTP_REFERER'])


# @login_required 
# def order_total_price(request, order_id)
#     items = OrderItem.filter
