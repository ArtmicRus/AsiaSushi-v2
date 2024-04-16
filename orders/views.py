from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect, render

from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem, OrderStatus
from orders.utils import create_statuses

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
                    cart_items = Cart.objects.filter(user=user)

                    if cart_items.exists():
                        # Проверяем есть ли стутусы
                        start_status = OrderStatus.objects.filter(name='В обработке')
                        if not start_status: # если статусов нет то создаём
                            create_statuses()

                        # Создать заказ
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'],
                            order_status_id=1,
                        )
                        # Создать заказанные товары
                        for cart_item in cart_items:
                            product=cart_item.product
                            name=cart_item.product.name
                            price=cart_item.product.self_price()
                            quantity=cart_item.quantity


                            # Количество товаров но так как вырезал количество то не нужно
                            # if product.quantity < quantity:
                            #     raise ValidationError(f'Недостаточное количество товара {name} на складе\
                            #                            В наличии - {product.quantity}')

                            # product.quantity -= quantity
                            # product.save()

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
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
            'last_name': request.user.last_name,
            }

        # initial = изначальные данные куда мы передаём предзаполненные данные
        # для авторизованных пользователей
        form = CreateOrderForm(initial=initial)

    context = {
        'title': 'Home - Оформление заказа',
        'form': form,
        'order': True,
    }
    return render(request, 'orders/create_order.html', context=context)
