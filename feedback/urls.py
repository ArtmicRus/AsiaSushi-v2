from django.urls import path

from feedback import views

app_name = 'feedback'

urlpatterns = [
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/create-review/', views.create_review, name='create_review'),
    path('reviews/change-review/<int:review_id>', views.change_review, name='change_review'),
    path('reviews/delete-review/<int:review_id>', views.delete_review, name='delete_review'),
    
    path('reviews/create-answer/<int:review_id>', views.create_answer, name='create_answer'),
]