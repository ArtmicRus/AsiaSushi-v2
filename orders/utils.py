from orders.models import OrderStatus

# Утилита создания базовых статусов заказа
def create_statuses():
    OrderStatus.objects.create(
        id=1,
        name='В обработке',
    )
    OrderStatus.objects.create(
        id=2,
        name='Готовится',
    )
    OrderStatus.objects.create(
        id=3,
        name='В пути',
    )
    OrderStatus.objects.create(
        id=4,
        name='Готов к выдаче',
    )
    OrderStatus.objects.create(
        id=5,
        name='Доставлен',
    )
    OrderStatus.objects.create(
        id=6,
        name='Отменён',
    )