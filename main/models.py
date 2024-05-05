from django.db import models

# Create your models here.
class Promotions(models.Model):

    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='promotions_images', blank=True, null=True, verbose_name='Изображение')
    # promo = models.CharField(max_length=10, verbose_name='Промокод для добавления акции к карзине')
    # promotion_terms = models.ForeignKey(to=PromotionTerms, on_delete=models.CASCADE,verbose_name='Условия акции')

    class Meta: 
        # Название таблицы в БД
        db_table = 'Promotions'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'

    def __str__(self) -> str:
        return f'{self.name}'