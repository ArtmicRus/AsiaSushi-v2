from django.db import models

from goods.models import Products
from promotions.models import Promotion
from users.models import User

# Принимает Кверисет - то есть несколько или один объект в его обётке
# По сути это как список
class CartItemQueryset(models.QuerySet):
    
    def total_price(self):
        return sum(cart_item.products_price() for cart_item in self)
    
    def total_quantity(self):
        if self:
            return sum(cart_item.quantity for cart_item in self)
        return 0
    
# Корзина пользователя
class Cart(models.Model):

    promotion = models.ForeignKey(to=Promotion, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Акция')

    class Meta:
        db_table = 'Carts'
        verbose_name = "Корзина"
        verbose_name_plural = "Корзина"

# Элементы корзины 
class CartItem(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE,blank=True, null=True, verbose_name='Пользователь')
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE,blank=True, null=True, verbose_name='Корзина')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE,verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    # Ключ сессии для того чтобы можно было записать действия неавторизованного пользователя
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'CartItems'
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"

    objects = CartItemQueryset().as_manager()

    def products_price(self): # посчитать суммарную стоимость товара в карзине
        return round(self.product.self_price() * self.quantity, 2)

    def get_cart(self):
        return self.cart

    def __str__(self): # В каком виде выводить информацию
        if self.user:
            return f"Корзина {self.user.username} | Товар {self.product.name} | Количество {self.quantity}"
        
        return f"Анонимная корзина Товар {self.product.name} | Количество {self.quantity}"
    
