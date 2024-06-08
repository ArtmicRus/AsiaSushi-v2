from django.urls import path

from promotions import views

app_name = 'promotions'

urlpatterns = [
    path('', views.promotions, name='promotions'),
    path('promotions_add_to_cart/', views.promotion_add_to_cart, name='promotion_add_to_cart'),
    path('promotions_delete_from_cart/', views.promotion_delete_from_cart, name='promotion_delete_from_cart'),
]