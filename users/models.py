from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to="users_image", blank=True, null=True, verbose_name='Аватар')
    phone_number = models.CharField(max_length=14, blank=True, null=True)

    class Meta: 
        # Название таблицы в БД
        db_table = 'user'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
