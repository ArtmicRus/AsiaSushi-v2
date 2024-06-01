from django.contrib import admin

from carts.models import CartItem

# admin.site.register(Cart)


# Класс для вывода в админке связанных с карзиной строк заказа
class CartTabAdmin(admin.TabularInline):
    
    # Модель карзины
    model = CartItem

    # Поля для отображения
    fields = [
        'product',
        'quantity',
        'created_timestamp',
    ]

    search_fields = [
        'product',
        'quantity',
        'created_timestamp',
    ]

    # Поле время создания только для чления
    readonly_fields = ('created_timestamp',)
    
    # Одно доп поле если необходимо добавить что то
    extra = 1

@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    # Вывод полей модели в админке
    list_display = [
        'user_display',
        'product_display',
        'quantity',
        'created_timestamp',
    ]

    list_filter = [
        "created_timestamp",
        "user",
        "product__name",
    ]

    # Для красивого отображения пользователя а не по его str методу
    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return "Анонимный пользователь"

    # Для красивого отображения продукта а не по его str методу
    def product_display(self, obj):
        return str(obj.product.name)



