from django import forms

from app.settings import SCORES


class CreateReviewForm(forms.Form):
    name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    email = forms.CharField(required=False)
    title = forms.CharField()
    message = forms.CharField()
    score = forms.ChoiceField(choices=SCORES)


class CreateAnswerForm(forms.Form):
    answer = forms.CharField()


class CreateFeedbackForm(forms.Form):
    email = forms.CharField(required=False)
    title = forms.CharField()
    message = forms.CharField()
    score = forms.ChoiceField(choices=SCORES)

