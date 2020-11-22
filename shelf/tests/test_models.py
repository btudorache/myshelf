from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Shelf, ShelfRow, ShelfItem
from books.models import Author, Book


class ShelfModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')

    def test_create_shelf_instance(self):
        shelf = Shelf.objects.create(owner=self.user)
        self.assertEquals(shelf, Shelf.objects.first())

    def test_shelf_get_absolute_url(self):
        shelf = Shelf.objects.create(owner=self.user)
        self.assertEquals(shelf.get_absolute_url(), f'/shelf/lists/{self.user.id}/')

    def test_shel_add_new_user_shelf_function(self):
        Shelf.add_new_user_shelf(self.user)
        self.assertEquals(Shelf.objects.first(), Shelf.objects.get(owner=self.user))
        self.assertEquals(len(ShelfRow.objects.all()), 3)

    def test_shelf_method_get_shelves(self):
        Shelf.add_new_user_shelf(self.user)
        shelf = Shelf.objects.get(owner=self.user)
        self.assertEquals(len(shelf.get_shelves()), 3)


class ShelfRowModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.shelf = Shelf.objects.create(owner=self.user)

    def test_create_shelf_row_instance(self):
        shelf_row = ShelfRow.objects.create(owner=self.user, name='new shelf row', shelf=self.shelf)
        self.assertEquals(shelf_row, ShelfRow.objects.first())

    def test_shelf_row_get_absolute_url(self):
        shelf_row = ShelfRow.objects.create(owner=self.user, name='new shelf row', shelf=self.shelf)
        self.assertEquals(shelf_row.get_absolute_url(), f'/shelf/lists/row/{shelf_row.id}/')

    def test_shelf_row_get_items_method(self):
        shelf_row = ShelfRow.objects.create(owner=self.user, name='new shelf row', shelf=self.shelf)
        author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        book1 = Book.objects.create(title='book1', author=author)
        book2 = Book.objects.create(title='book2', author=author)
        book3 = Book.objects.create(title='book3', author=author)
        shelf_item1 = ShelfItem.objects.create(owner=self.user, shelf_row=shelf_row, book=book1)
        shelf_item2 = ShelfItem.objects.create(owner=self.user, shelf_row=shelf_row, book=book2)
        shelf_item3 = ShelfItem.objects.create(owner=self.user, shelf_row=shelf_row, book=book3)

        items = shelf_row.get_items()
        self.assertEquals(items[0], shelf_item1)
        self.assertEquals(items[1], shelf_item2)
        self.assertEquals(items[2], shelf_item3)

    def test_shelf_row_increment_and_decrement(self):
        shelf_row = ShelfRow.objects.create(owner=self.user, name='new shelf row', shelf=self.shelf)

        shelf_row.shelf_item_add()
        self.assertEquals(shelf_row.num_items, 1)
        shelf_row.shelf_item_delete()
        self.assertEquals(shelf_row.num_items, 0)


class ShelfItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.shelf = Shelf.objects.create(owner=self.user)
        self.shelf_row = ShelfRow.objects.create(owner=self.user, name='new shelf row', shelf=self.shelf)

    def test_create_shelf_row_item_instance(self):
        author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        book = Book.objects.create(title='Crime And Punishment', author=author)
        shelf_item = ShelfItem.objects.create(owner=self.user, shelf_row=self.shelf_row, book=book)
        self.assertEquals(shelf_item, ShelfItem.objects.first())

    def test_get_shelf_item_method_1(self):
        author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        book = Book.objects.create(title='Crime And Punishment', author=author)
        ShelfItem.objects.create(owner=self.user, shelf_row=self.shelf_row, book=book)
        shelf_item = ShelfItem.get_shelf_item(self.user, book)
        self.assertEquals(shelf_item, ShelfItem.objects.first())

    def test_get_shelf_item_method_2(self):
        author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        book = Book.objects.create(title='Crime And Punishment', author=author)
        self.assertTrue(ShelfItem.get_shelf_item(self.user, book) is None)
