from django.urls import path

from promotions import views

app_name = 'promotions'

urlpatterns = [
    path('', views.promotions, name='promotions'),
    path('promotions_add_to_cart/', views.promotions_add_to_cart, name='promotions_add_to_cart'),
    path('promotions_delete_from_cart/', views.promotions_delete_from_cart, name='promotions_delete_from_cart'),
]