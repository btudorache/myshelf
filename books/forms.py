from django import forms

from .models import BookRating


class BookRateForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ('rate',)