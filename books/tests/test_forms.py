from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import BookRateForm, BookReviewForm, SearchForm

from ..models import Genre, Author, Book, BookRating, BookReview


class BookRateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='testing1234')
        self.genre = Genre.objects.create(genre='Action', description='best genre ever')
        self.author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        self.book = Book.objects.create(title='Crime And Punishment', author=self.author)
        self.book.genre.add(self.genre)

    def test_book_rate_form_creates_object(self):
        form = BookRateForm(data={'rate': 5})
        self.assertEquals(form.is_valid(), True)
        rating = form.save(commit=False)
        rating.rated_by = self.user
        rating.book_rated = self.book
        rating.save()
        self.assertEquals(rating, BookRating.objects.first())


class BookReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='testing1234')
        self.genre = Genre.objects.create(genre='Action', description='best genre ever')
        self.author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        self.book = Book.objects.create(title='Crime And Punishment', author=self.author)
        self.book.genre.add(self.genre)

    def test_book_review_form_creates_object(self):
        form = BookReviewForm(data={'text': 'this is the best book ever'})
        self.assertEquals(form.is_valid(), True)
        review = form.save(commit=False)
        review.reviewer = self.user
        review.book_reviewed = self.book
        review.save()
        self.assertEquals(review, BookReview.objects.first())


class SearchFormTest(TestCase):
    def test_search_form(self):
        form = SearchForm(data={'query': 'moby dick'})
        self.assertEquals(form.is_valid(), True)
        self.assertEquals(form.cleaned_data['query'], 'moby dick')