from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from ..models import Book, Author, Genre, BookReview, BookRating
from ..forms import BookRateForm
from shelf.forms import ShelfItemForm
from shelf.models import Shelf


class BookSearchListViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(genre='Action')
        self.author = Author.objects.create(last_name='Dostoevsky')
        self.book = Book.objects.create(title='Crime and Punishment', author=self.author)
        self.book.genre.add(self.genre)
        user = User.objects.create_user(username='test_user', password='testing1234')
        self.client.login(username='test_user', password='testing1234')

    def test_all_books_list(self):
        response = self.client.get('/books/search/all/')
        self.assertEquals(response.status_code, 200)

    def test_all_books_list_gets_all_books(self):
        book2 = Book.objects.create(title='book2', author=self.author)
        book3 = Book.objects.create(title='book3', author=self.author)
        response = self.client.get('/books/search/all/')
        self.assertEquals(len(response.context['page_obj'].object_list), 3)

    def test_all_books_list_template(self):
        response = self.client.get('/books/search/all/')
        self.assertTemplateUsed(response, 'books/book_search_list.html')

    def test_get_book_by_genre(self):
        genre2 = Genre.objects.create(genre='Adventure')
        book2 = Book.objects.create(title='book2', author=self.author)
        book2.genre.add(genre2)
        response = self.client.get(f'/books/search/genre/{genre2.id}/')
        self.assertEquals(book2, response.context['page_obj'].object_list[0])

    def test_get_book_by_author(self):
        author2 = Author.objects.create(last_name='Eminescu')
        book2 = Book.objects.create(title='Luceafarul', author=author2)
        response = self.client.get(f'/books/search/author/{author2.id}/')
        self.assertEquals(book2, response.context['page_obj'].object_list[0])

    def test_get_book_by_search(self):
        data = {'query': 'dosto'}
        response = self.client.get('/books/search/', data)
        self.assertEquals(self.book, response.context['page_obj'].object_list[0])


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(genre='Action')
        self.author = Author.objects.create(last_name='Dostoevsky')
        self.book = Book.objects.create(title='Crime and Punishment', author=self.author)
        self.book.genre.add(self.genre)
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)
        self.rating = BookRating.objects.create(rated_by=self.user, rate=5, book_rated=self.book)
        self.review = BookReview.objects.create(book_reviewed=self.book, reviewer=self.user, text='best book ever')
        self.client.login(username='test_user', password='testing1234')
        self.request = self.client.get(f'/books/search/{self.book.id}/')

    def test_view_user_correct_template(self):
        self.assertTemplateUsed(self.request, 'books/book_detail.html')

    def test_view_gets_all_forms(self):
        self.assertIsInstance(self.request.context['book_rate_form'], (BookRateForm,))
        self.assertIsInstance(self.request.context['shelf_item_form'], (ShelfItemForm,))

    def test_view_gets_correct_rating(self):
        self.assertEquals(self.rating, self.request.context['rating'])

    def test_view_gets_correct_review(self):
        self.assertEquals(self.review, self.request.context['review'])


class BookRateCreateViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(genre='Action')
        self.author = Author.objects.create(last_name='Dostoevsky')
        self.book = Book.objects.create(title='Crime and Punishment', author=self.author)
        self.book.genre.add(self.genre)
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.client.login(username='test_user', password='testing1234')

    def test_book_rate_view_creates_book_rating(self):
        request = self.client.post(f'/books/rate/{self.book.id}/create/', data={'rate': 5})
        self.assertEquals(len(BookRating.objects.all()), 1)

    def test_book_rate_view_redirects_correctly(self):
        request = self.client.post(f'/books/rate/{self.book.id}/create/', data={'rate': 5})
        self.assertEquals(request.url, f'/books/search/{self.book.id}/')


class BookRateUpdateTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(genre='Action')
        self.author = Author.objects.create(last_name='Dostoevsky')
        self.book = Book.objects.create(title='Crime and Punishment', author=self.author)
        self.book.genre.add(self.genre)
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.book.num_ratings = 1
        self.book.average_rating = 5
        self.book.save()
        self.client.login(username='test_user', password='testing1234')

    def test_view_updates_rating(self):
        rating = BookRating.objects.create(rated_by=self.user, rate=5, book_rated=self.book)
        request = self.client.post(f'/books/rate/{self.book.id}/{rating.id}/update/', data={'rate': 2})
        rating = BookRating.objects.all().first()
        self.assertEquals(rating.rate, 2)

    def test_view_updates_book_average_rating(self):
        rating = BookRating.objects.create(rated_by=self.user, rate=5, book_rated=self.book)
        request = self.client.post(f'/books/rate/{self.book.id}/{rating.id}/update/', data={'rate': 2})
        book = Book.objects.get(id=self.book.id)
        self.assertEquals(book.average_rating, 2)

    def test_view_redirects_to_book_detail(self):
        rating = BookRating.objects.create(rated_by=self.user, rate=5, book_rated=self.book)
        request = self.client.post(f'/books/rate/{self.book.id}/{rating.id}/update/', data={'rate': 2})
        self.assertEquals(request.url, f'/books/search/{self.book.id}/')


class BookCreateReviewViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(genre='Action')
        self.author = Author.objects.create(last_name='Dostoevsky')
        self.book = Book.objects.create(title='Crime and Punishment', author=self.author)
        self.book.genre.add(self.genre)
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.client.login(username='test_user', password='testing1234')

    def test_book_review_create_gets_correct_template(self):
        request = self.client.get(f'/books/review/create/{self.book.id}/')
        self.assertTemplateUsed(request, 'books/book_create_review.html')

    def test_book_review_view_creates_review(self):
        request = self.client.post(f'/books/review/create/{self.book.id}/', data={'text': 'best book ever'})
        review = BookReview.objects.first()
        self.assertTrue(review)


class BookUpdateReviewViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(genre='Action')
        self.author = Author.objects.create(last_name='Dostoevsky')
        self.book = Book.objects.create(title='Crime and Punishment', author=self.author)
        self.book.genre.add(self.genre)
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.client.login(username='test_user', password='testing1234')

    def test_book_review_update_gets_correct_template(self):
        review = BookReview.objects.create(book_reviewed=self.book, reviewer=self.user, text='best book ever')
        request = self.client.get(f'/books/review/{self.book.id}/{review.id}/update/')
        self.assertTemplateUsed(request, 'books/book_update_review.html')

    def test_book_review_update_actually_updates_the_review(self):
        review = BookReview.objects.create(book_reviewed=self.book, reviewer=self.user, text='best book ever')
        request = self.client.post(f'/books/review/{self.book.id}/{review.id}/update/',
                                   data={'text': 'updated: best book ever'})
        review = BookReview.objects.first()
        self.assertEquals(review.text, 'updated: best book ever')
