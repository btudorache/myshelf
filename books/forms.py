from django import forms

from .models import BookRating, BookReview


class BookRateForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields = ('rate',)


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('text',)


class SearchForm(forms.Form):
    query = forms.CharField(label=False)
