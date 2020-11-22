from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import ShelfItemForm, ShelfRowForm
from ..models import Shelf, ShelfRow, ShelfItem
from books.models import Author, Book


class ShelfRowFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.shelf = Shelf.objects.create(owner=self.user)

    def test_shelf_row_form_creates_item(self):
        form = ShelfRowForm(data={'name': 'new_row'})
        new_row = form.save(commit=False)
        new_row.owner = self.user
        new_row.shelf = self.shelf
        new_row.save()
        self.assertEquals(new_row, ShelfRow.objects.first())


class ShelfItemFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        Shelf.add_new_user_shelf(self.user)

    def test_shelf_item_form_shows_correct_forms(self):
        form = ShelfItemForm(user=self.user)
        self.assertEquals(len(form.fields['shelf_row'].queryset), 3)

    def test_shelf_item_form_creates_item(self):
        author = Author.objects.create(first_name='Fyodor', last_name='Dostoevsky', description='Best author ever')
        book = Book.objects.create(title='Crime And Punishment', author=author)
        shelf_row = ShelfRow.objects.filter(owner=self.user.id)[0]
        form = ShelfItemForm(user=self.user, data={'shelf_row': shelf_row})
        new_item = form.save(commit=False)
        new_item.owner = self.user
        new_item.book = book
        new_item.save()
        self.assertEquals(new_item, ShelfItem.objects.first())