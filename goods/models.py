from django.db import models
from django.urls import reverse

class Categories(models.Model):
    # verbose_name отображает в админке при создании объекта
    name = models.CharField(max_length=150,unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta: 
        # Название таблицы в БД
        db_table = 'Categories'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name

# class PromotionTerms(models.Model):

#     is_need_min_sum_in_cart = models.BooleanField(default=False, verbose_name='Нужна ли минимальная сумма в заказе')
#     min_sum_in_cart = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Минимальная сумма в заказе')

#     is_need_exclude_caregory = models.BooleanField(default=False, verbose_name='Нужно ли Исключить товары определённой категории из акции')
#     exclude_caregory = category = models.ForeignKey(to=Categories, on_delete=models.CASCADE,verbose_name='Исключаемая категория')



    # class Meta: 
    #     # Название таблицы в БД
    #     db_table = 'promotionTerms'
    #     # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
    #     verbose_name = 'Условия акции'
    #     verbose_name_plural = 'Условия акции'

class Products(models.Model):

    # verbose_name отображает в админке при создании объекта
    name = models.CharField(max_length=150,unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Скидка в %')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE,verbose_name='Категория')

    class Meta: 
        # Название таблицы в БД
        db_table = 'Products'
        # Имя которые мы хотим в админке (Альтернативное имя) для единственного и множ числа
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ("id",)
    
    def __str__(self) -> str:
        return f'{self.name}'
    
    def get_absolute_url(self):
        return reverse("catalog:product", kwargs={"product_slug": self.slug})
    

    def display_id(self):
        return f"{self.id:05}"
    
    def self_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)
        
        return self.price
