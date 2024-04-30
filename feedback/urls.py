from django.urls import path

from feedback import views

app_name = 'feedback'

urlpatterns = [
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/create-review/', views.create_review, name='create_review'),
    path('reviews/create-answer/<int:review_id>', views.create_answer, name='create_answer'),
]