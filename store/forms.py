from django import forms
from .models import ReviewRaiting

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRaiting
        fields = ['subject', 'review', 'rating']
