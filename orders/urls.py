from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('create-order/', views.create_order, name='create_order'),
    path('delete-order/<int:order_id>', views.delete_order, name='delete_order')
]