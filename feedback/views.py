from datetime import datetime
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import redirect, render

from django.contrib.auth.decorators import login_required
from app.settings import SCORES
from feedback.forms import ChangeReviewForm, CreateAnswerForm, CreateReviewForm
from feedback.models import Reviews

# Create your views here.
def reviews(request):

    reviews = Reviews.objects.all()
    # Если пользователь авторизован то берём данные для автозаполнения формы
    if request.user.is_authenticated:
        initial = {
            'name': request.user.first_name,
            'email': request.user.email,
            'phone_number': request.user.phone_number,
        }

        # initial = изначальные данные куда мы передаём предзаполненные данные
        # для авторизованных пользователей
        form = CreateReviewForm(initial=initial)

        context = {
            "title": "Asia - Отзывы",
            'form': form,
            'scores':SCORES,
            "year": datetime.now().year,
            "reviews": reviews,
        }
    # Иначе берём всю информацию не нужную для формы отзыва
    else:
        context = {
            "title": "Asia - Отзывы",
            "year": datetime.now().year,
            "reviews": reviews,
        }
    
    return render(request, "feedback/reviews.html", context)

@login_required
def create_review(request):

    if request.method == 'POST':
        form = CreateReviewForm(data=request.POST)
        if form.is_valid():
            user = request.user
            try:
                Reviews.objects.create(
                        user=user,
                        title=form.cleaned_data['title'],
                        comment=form.cleaned_data['message'],
                        score=form.cleaned_data['score'],
                    )
                
                messages.success(request, 'Ваш отзыв успешно опубликован!')
            
            except ValidationError as e:
                messages.success(request, str(e))
        else:
            messages.success(request, form.errors)
    

    return redirect('feedback:reviews')


@login_required
def create_answer(request, review_id):
    
    if request.method == 'POST':
        form = CreateAnswerForm(data=request.POST)
        if form.is_valid():
            try:
                review = Reviews.objects.get(pk = review_id)
                review.answer = form.cleaned_data['answer']

                review.save()
                messages.success(request, 'Ваш ответ на отзыв успешно опубликован!')

            except ValidationError as e:
                messages.success(request, str(e))
        else:
            messages.success(request, form.errors)
    
    return redirect('feedback:reviews')

@login_required
def change_review(request, review_id):

    if request.method == 'POST':
        form = ChangeReviewForm(data=request.POST)
        if form.is_valid():
            try:
                review = Reviews.objects.get(id=review_id)

                review.title = form.cleaned_data['title']
                review.comment = form.cleaned_data['message']
                review.score = form.cleaned_data['score_changes']

                review.save()
                
                messages.success(request, 'Ваш отзыв успешно изменён!')
            
            except ValidationError as e:
                messages.success(request, str(e))
        else:
            messages.success(request, form.errors)
    

    return redirect('feedback:reviews')

@login_required
def delete_review(request, review_id):
    Reviews.objects.get(id=review_id).delete()
    return redirect('feedback:reviews')

