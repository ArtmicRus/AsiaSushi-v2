from orders.models import Status


def create_statuses():
    Status.objects.create(
        id=1,
        name='В обработке',
    )
    Status.objects.create(
        id=2,
        name='Готовится',
    )
    Status.objects.create(
        id=3,
        name='В пути',
    )
    Status.objects.create(
        id=4,
        name='Готов к выдаче',
    )
    Status.objects.create(
        id=5,
        name='Доставлен',
    )
    Status.objects.create(
        id=6,
        name='Отменён',
    )