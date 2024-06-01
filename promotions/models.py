from django.db import models

# Create your models here.
from goods.models import Products

# Create your models here.
class PromotionTerms(models.Model):

    is_need_min_price = models.BooleanField(default=False, verbose_name='Нужна ли минимальная сумма в заказе')
    min_price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Минимальная сумма в заказе для добавления акции')

    # is_need_exclude_caregory = models.BooleanField(default=False, verbose_name='Нужно ли Исключить товары определённой категории из акции')
    # exclude_caregory = category = models.ForeignKey(to=Categories, on_delete=models.CASCADE,verbose_name='Исключаемая категория')

    class Meta: 
        # Название таблицы в БД
        db_table = 'PromotionTerms'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Условие акции'
        verbose_name_plural = 'Условия акции'


class Promotion(models.Model):

    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='promotions_images', blank=True, null=True, verbose_name='Изображение')
    # promo = models.CharField(max_length=10, verbose_name='Промокод для добавления акции к карзине')
    promotion_terms = models.ForeignKey(to=PromotionTerms, on_delete=models.PROTECT ,verbose_name='Условия акции')

    class Meta: 
        # Название таблицы в БД
        db_table = 'Promotions'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self) -> str:
        return f'{self.name}'

class PromotionProducts(models.Model):

    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, null=True, verbose_name="Акционный продукт", default=None)
    promotion = models.ForeignKey(to=Promotion, on_delete=models.PROTECT, null=True, verbose_name='Акция', default=None)

    class Meta: 
        # Название таблицы в БД
        db_table = 'PromotionProducts'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Акционный товар'
        verbose_name_plural = 'Товары для акций'
