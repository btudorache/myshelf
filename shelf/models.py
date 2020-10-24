from django.conf import settings
from django.db import models

from books.models import Book


class Shelf(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='shelf',
                              on_delete=models.CASCADE)


class ShelfRow(models.Model):
    name = models.CharField(max_length=20)
    shelf = models.ForeignKey(Shelf,
                              related_name='row',
                              on_delete=models.CASCADE)


class ShelfItem(models.Model):
    datetime = models.DateField(auto_now_add=True)
    shelfRow = models.ForeignKey(ShelfRow,
                                 related_name='books',
                                 on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             related_name='row_items',
                             on_delete=models.CASCADE)