from unicodedata import category
from django.db import models

class Categories(models.Model):
    # verbose_name отображает в админке при создании объекта
    name = models.CharField(max_length=150,unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta: 
        # Название таблицы в БД
        db_table = 'category'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name

class Products(models.Model):

    # verbose_name отображает в админке при создании объекта
    name = models.CharField(max_length=150,unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveBigIntegerField(default=0,verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE,verbose_name='Категория')

    class Meta: 
        # Название таблицы в БД
        db_table = 'product'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
    
    def __str__(self) -> str:
        return f'{self.name} Количество - {self.quantity}'
    
    def display_id(self):
        return f"{self.id:05}"
    
    def self_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        
        return self.price
