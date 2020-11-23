from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Shelf, ShelfRow, ShelfItem
from ..forms import ShelfRowForm

from books.models import Author, Book
from actions.models import Action


class ShelfListsViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)
        self.client.login(username='test_user', password='testing1234')

    def test_view_gets_correct_template(self):
        request = self.client.get(f'/shelf/lists/{self.user.id}/')
        self.assertTemplateUsed(request, 'shelf/shelf_lists.html')

    def test_view_gets_correct_context(self):
        request = self.client.get(f'/shelf/lists/{self.user.id}/')
        shelf = request.context['shelf']
        self.assertEquals(shelf, Shelf.objects.get(owner=self.user))
        shelf_rows = request.context['shelf_rows']
        self.assertEquals(list(shelf_rows), list(Shelf.get_shelves(shelf)))
        self.assertEquals(request.context['section'], 'shelf')


class ShelfRowItemsViesTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)

        self.shelf_row = ShelfRow.objects.filter(owner=self.user)[0]
        author = Author.objects.create(last_name='test_author')
        book1 = Book.objects.create(title='test_book1', author=author)
        self.item1 = ShelfItem.objects.create(owner=self.user, shelf_row=self.shelf_row, book=book1)
        book2 = Book.objects.create(title='test_book2', author=author)
        self.item2 = ShelfItem.objects.create(owner=self.user, shelf_row=self.shelf_row, book=book2)

        self.client.login(username='test_user', password='testing1234')

    def test_view_gets_correct_template(self):
        request = self.client.get(f'/shelf/lists/row/{self.shelf_row.id}/')
        self.assertTemplateUsed(request, 'shelf/shelf_row_items.html')

    def test_view_gets_correct_context(self):
        request = self.client.get(f'/shelf/lists/row/{self.shelf_row.id}/')
        shelf = request.context['shelf']
        self.assertEquals(shelf, Shelf.objects.get(owner=self.user))
        shelf_row = request.context['row']
        self.assertEquals(shelf_row, ShelfRow.objects.get(id=self.shelf_row.id))
        shelf_items = request.context['page_obj'].object_list
        self.assertEquals(list(shelf_items), list(ShelfItem.objects.filter(owner=self.user)))
        self.assertEquals(request.context['section'], 'shelf')


class AddShelfItemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)
        self.shelf_row = ShelfRow.objects.filter(owner=self.user)[0]

        author = Author.objects.create(last_name='test_author')
        self.book = Book.objects.create(title='test_book1', author=author)

        self.client.login(username='test_user', password='testing1234')

    def test_view_creates_new_instance(self):
        request = self.client.post(f'/shelf/add/{self.book.id}/', data={'shelf_row': self.shelf_row.id})
        item = ShelfItem.objects.all()[0]
        self.assertTrue(item is not None)

    def test_view_creates_new_action(self):
        request = self.client.post(f'/shelf/add/{self.book.id}/', data={'shelf_row': self.shelf_row.id})
        action = Action.objects.all()[0]
        self.assertTrue(action is not None)

    def test_view_correct_redirect(self):
        request = self.client.post(f'/shelf/add/{self.book.id}/', data={'shelf_row': self.shelf_row.id})
        self.assertEquals(request.url, self.book.get_absolute_url())


class UpdateShelfItemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)
        self.shelf_row1 = ShelfRow.objects.filter(owner=self.user)[0]
        self.shelf_row2 = ShelfRow.objects.filter(owner=self.user)[1]

        author = Author.objects.create(last_name='test_author')
        self.book = Book.objects.create(title='test_book1', author=author)
        self.item = ShelfItem.objects.create(owner=self.user, shelf_row=self.shelf_row1, book=self.book)

        self.client.login(username='test_user', password='testing1234')

    def test_view_updates_old_item(self):
        request = self.client.post(f'/shelf/update/{self.book.id}/{self.item.id}/',
                                   data={'shelf_row': self.shelf_row2.id})
        item = ShelfItem.objects.all()[0]
        self.assertEquals(item.shelf_row, self.shelf_row2)

    def test_view_deletes_old_item(self):
        request = self.client.post(f'/shelf/update/{self.book.id}/{self.item.id}/',
                                   data={'shelf_row': self.shelf_row2.id})
        self.assertFalse(ShelfItem.objects.filter(shelf_row=self.shelf_row1))

    def test_view_correct_redirect(self):
        request = self.client.post(f'/shelf/update/{self.book.id}/{self.item.id}/',
                                   data={'shelf_row': self.shelf_row2.id})
        self.assertEquals(request.url, self.book.get_absolute_url())


class DeleteShelfItemViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)
        self.shelf_row = ShelfRow.objects.filter(owner=self.user)[0]

        author = Author.objects.create(last_name='test_author')
        self.book = Book.objects.create(title='test_book1', author=author)
        self.item = ShelfItem.objects.create(owner=self.user, shelf_row=self.shelf_row, book=self.book)

        self.client.login(username='test_user', password='testing1234')

    def test_delete_instance_for_books_app(self):
        self.client.get(f'/shelf/delete/{self.item.id}/search/')
        self.assertFalse(ShelfItem.objects.all())

    def test_delete_instance_for_shelf_app(self):
        self.client.get(f'/shelf/delete/{self.item.id}/shelf/')
        self.assertFalse(ShelfItem.objects.all())

    def test_delete_for_books_app_correct_redirect(self):
        response = self.client.get(f'/shelf/delete/{self.item.id}/search/')
        self.assertEquals(response.url, self.book.get_absolute_url())

    def test_delete_for_shelf_app_correct_redirect(self):
        response = self.client.get(f'/shelf/delete/{self.item.id}/shelf/')
        self.assertEquals(response.url, self.shelf_row.get_absolute_url())


class AddShelfViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)
        self.client.login(username='test_user', password='testing1234')

    def test_get_request_gets_correct_template(self):
        request = self.client.get('/shelf/add/shelf_row/')
        self.assertTemplateUsed(request, 'shelf/shelf_row_add.html')

    def test_get_request_gets_correct_context(self):
        request = self.client.get('/shelf/add/shelf_row/')
        self.assertIsInstance(request.context['shelf_row_form'], ShelfRowForm)
        self.assertEquals(request.context['section'], 'shelf')

    def test_post_request_creates_new_instance(self):
        request = self.client.post('/shelf/add/shelf_row/', data={'name': 'new_row'})
        self.assertTrue(ShelfRow.objects.get(name='new_row'))

    def test_post_request_redirects(self):
        request = self.client.post('/shelf/add/shelf_row/', data={'name': 'new_row'})
        self.assertEquals(request.url, self.user.user_shelf.get_absolute_url())


class DeleteShelfRowViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)
        self.shelf = ShelfRow.objects.create(owner=self.user, name='test_shelf', shelf=self.user.user_shelf)
        self.client.login(username='test_user', password='testing1234')

    def test_delete_not_default_shelf(self):
        request = self.client.get(f'/shelf/delete/{self.shelf.id}/')
        self.assertEquals(len(list(ShelfRow.objects.all())), 3)

    def test_delete_default_shelf(self):
        default_shelf = ShelfRow.objects.all()[0]
        request = self.client.get(f'/shelf/delete/{default_shelf.id}/')
        self.assertEquals(len(list(ShelfRow.objects.all())), 4)

    def test_view_redirects(self):
        request = self.client.get(f'/shelf/delete/{self.shelf.id}/')
        self.assertEquals(request.url, self.user.user_shelf.get_absolute_url())