from django.apps import AppConfig


class GoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goods'
    # Название раздела в админке
    verbose_name= 'Товары'
