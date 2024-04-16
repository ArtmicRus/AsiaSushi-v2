from django.contrib import admin

from goods.models import Categories, Products

#admin.site.register(Categories)
#admin.site.register(Products)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
        # Вывод полей модели в админке
    list_display = [
        'name'
    ]

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    # Автозаполнение slug при создании товара в админке
    prepopulated_fields = {'slug': ('name',)}

    # Вывод полей модели в админке
    list_display = [
        'name',
        'price',
        'discount'
    ]

    # Поля которые можно редактировать в админке
    list_editable = [
        'discount',
    ]

    # Добавляет поле Поиск в админке по указанным полям
    search_fields = [
        'name',
        'description'
    ]

    # Добавляет фильтры справа в админке по указанным полям
    list_filter = [
        'discount', 
        'category'
    ]

    # Указывает порядок отображаемых полей в админке
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        # Если надо в 1 строку
        ("price","discount"),
    ]
    