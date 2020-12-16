import os
from time import sleep

from django.test import TestCase
# Used for mock test
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from myshelf.settings import MEDIA_ROOT

from ..models import Genre, Author, Book, BookRating, BookReview


class GenreModelTest(TestCase):
    def test_genre_create(self):
        genre = Genre.objects.create(genre='Action', description='best genre ever')
        self.assertEquals(genre, Genre.objects.first())
        self.assertEquals(genre.description, 'best genre ever')

    def test_default_genre_create(self):
        genre = Genre.objects.create(genre='Action')
        self.assertEquals(genre.genre, 'Action')
        self.assertEquals(genre, Genre.objects.first())


class AuthorModelTest(TestCase):
    def test_create_author_last_name_only(self):
        author = Author.objects.create(last_name='Dostoevsky')
        self.assertEquals(author.last_name, 'Dostoevsky')
        self.assertEquals(author, Author.objects.first())

    def test_create_author_full_fields(self):
        author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        self.assertEquals(author, Author.objects.first())
        self.assertEquals(author.first_name, 'Fyodor')
        self.assertEquals(author.last_name, 'Dostoevsky')
        self.assertEquals(author.description, 'Best author ever')


class BookModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(genre='Action', description='best genre ever')
        self.author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        self.book = Book.objects.create(title='Crime And Punishment', author=self.author)
        self.book.genre.add(self.genre)

    def test_create_default_book(self):
        self.assertEquals(self.book, Book.objects.first())

    def test_book_has_correct_author(self):
        self.assertEquals(self.book.author, self.author)

    def test_book_has_correct_genre(self):
        self.assertEquals(self.book.genre.first(), self.genre)

    def test_book_has_correct_default_cover(self):
        self.assertEquals(self.book.cover.name, 'default_book.jpg')

    def test_book_has_correct_default_values(self):
        self.assertEquals(self.book.num_ratings, 0)
        self.assertEquals(self.book.average_rating, 0)

    def test_get_absolute_url(self):
        self.assertEquals(self.book.get_absolute_url(), f'/books/search/{self.book.id}/')

    def test_book_with_more_genres(self):
        new_book = Book.objects.create(title='Crime And Punishment', author=self.author)
        genre_drama = Genre.objects.create(genre='Drama')
        new_book.genre.add(self.genre)
        new_book.genre.add(genre_drama)
        self.assertEquals(new_book.genre.count(), 2)
        self.assertEquals(new_book.genre.first(), self.genre)
        self.assertEquals(new_book.genre.last(), genre_drama)

    # test only works on windows
    def test_book_with_custom_cover(self):
        new_book = Book.objects.create(title='Crime And Punishment', author=self.author)
        new_book.genre.add(self.genre)
        new_book.cover = SimpleUploadedFile(name='test_image.jpg',
                                            content=open(MEDIA_ROOT + '/default_profile.jpg', 'rb').read(),
                                            content_type='image/jpeg')
        new_book.save()
        self.assertEquals(new_book.cover.name, 'book_covers/test_image.jpg')
        self.assertEquals(new_book.cover.path, MEDIA_ROOT[:-1] + '\\book_covers\\test_image.jpg')
        os.remove(MEDIA_ROOT + 'book_covers\\test_image.jpg')

    def test_create_search_query_method(self):
        book1 = Book.objects.create(title='Crime and Punishment', author=self.author)
        book2 = Book.objects.create(title='Crime and Payment', author=self.author)
        book3 = Book.objects.create(title='The Brothers Karamazov', author=self.author)
        books = Book.objects.filter(Book.create_search_query("Crime".split()))
        self.assertTrue(book1 in books)
        self.assertTrue(book2 in books)
        self.assertFalse(book3 in books)

    def test_book_add_new_rating(self):
        book = Book.objects.create(title="New book", author=self.author)
        book.add_value_to_rating(8)
        self.assertEquals(book.average_rating, 8)
        self.assertEquals(book.num_ratings, 1)

    def test_book_add_more_ratings(self):
        book = Book.objects.create(title="New book", author=self.author)
        book.add_value_to_rating(8)
        book.add_value_to_rating(2)
        book.add_value_to_rating(5)
        self.assertEquals(book.average_rating, 5)
        self.assertEquals(book.num_ratings, 3)

    def test_book_update_rating(self):
        book = Book.objects.create(title="New book", author=self.author)
        book.add_value_to_rating(8)
        book.add_value_to_rating(2)
        book.add_value_to_rating(5)
        book.update_rating_delete(5)
        book.update_rating_add(8)

        self.assertEquals(book.average_rating, 6)
        self.assertEquals(book.num_ratings, 3)


class BookRatingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='testing1234')
        self.author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        self.book = Book.objects.create(title="New book", author=self.author)
        self.rating = BookRating.objects.create(rated_by=self.user, rate=4, book_rated=self.book)

    def test_create_book_rating(self):
        self.assertEquals(self.rating, BookRating.objects.first())

    def test_book_rating_has_correct_foreign_keys(self):
        self.assertEquals(self.user, self.rating.rated_by)
        self.assertEquals(self.book, self.rating.book_rated)

    def test_1_get_book_rating_method(self):
        rating = BookRating.get_book_rating(self.user, self.book)
        self.assertEquals(self.rating, rating)

    def test_2_get_book_rating_method(self):
        new_book = Book.objects.create(title="book with no rating", author=self.author)
        new_rating = BookRating.get_book_rating(self.user, new_book)
        self.assertFalse(new_rating)


class BookReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='testing1234')
        self.author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        self.book = Book.objects.create(title="New book", author=self.author)
        self.review = BookReview.objects.create(book_reviewed=self.book,
                                                reviewer=self.user,
                                                text='test review')
        sleep(0.5)

    def test_create_book_review(self):
        self.assertEquals(self.review, BookReview.objects.first())
        self.assertEquals(self.review.text, 'test review')

    def test_book_rating_has_correct_foreign_keys(self):
        self.assertEquals(self.review.book_reviewed, self.book)
        self.assertEquals(self.review.reviewer, self.user)

    def test_get_absolute_url(self):
        self.assertEquals(self.review.get_absolute_url(), f'/books/review/{self.review.id}/')

    def test_1_get_book_rating_method(self):
        new_review = BookReview.get_book_review(self.user, self.book)
        self.assertEquals(new_review, self.review)

    def test_2_get_book_rating_method(self):
        new_book = Book.objects.create(title="book with no review", author=self.author)
        new_review = BookReview.get_book_review(self.user, new_book)
        self.assertFalse(new_review)

    # Must sleep between review.create() so datetime ordering can happen correctly
    def test_book_rating_ordering(self):
        review1 = BookReview.objects.create(book_reviewed=self.book,
                                            reviewer=self.user,
                                            text='test review number 1')
        sleep(0.5)
        review2 = BookReview.objects.create(book_reviewed=self.book,
                                            reviewer=self.user,
                                            text='test review number 2')
        sleep(0.5)
        review3 = BookReview.objects.create(book_reviewed=self.book,
                                            reviewer=self.user,
                                            text='test review number 3')
        sleep(0.5)
        reviews = BookReview.objects.all()
        self.assertEquals(reviews[0], review3)
        self.assertEquals(reviews[1], review2)
        self.assertEquals(reviews[2], review1)