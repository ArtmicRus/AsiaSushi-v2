from django.db import models

from app.settings import SCORES
from users.models import User

# Create your models here.
class Reviews(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, blank=True, null=False, verbose_name="Пользователь", default=None)
    title = models.CharField(max_length=25, blank=False, null=True, verbose_name='Заголовок отзыва')
    comment = models.TextField(max_length=500, blank=False, null=True, verbose_name='Текст отзыва')
    answer = models.TextField(max_length=200, blank=False, null=True, verbose_name='Текст ответа на отзыв')
    score = models.PositiveSmallIntegerField(choices=SCORES, verbose_name='Оценка от пользователя')
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации отзыва")

    class Meta: 
        # Название таблицы в БД
        db_table = 'Reviews'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ("id",)
