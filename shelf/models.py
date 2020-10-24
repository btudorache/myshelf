from django.conf import settings
from django.db import models

from books.models import Book


class Shelf(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='shelf',
                              on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.username}'s shelf"

    def get_shelves(self):
        return ShelfRow.objects.filter(shelf=self)

    @staticmethod
    def add_new_user_shelf(new_user):
        new_shelf = Shelf.objects.create(owner=new_user)
        ShelfRow.objects.create(name="Read", shelf=new_shelf)
        ShelfRow.objects.create(name="Currently Reading", shelf=new_shelf)
        ShelfRow.objects.create(name="Want to Read", shelf=new_shelf)


class ShelfRow(models.Model):
    name = models.CharField(max_length=20)
    shelf = models.ForeignKey(Shelf,
                              related_name='row',
                              on_delete=models.CASCADE)
    num_items = models.IntegerField(default=0)

    def __str__(self):
        return f"Row {self.name} in {self.shelf.owner.username}'s shelf"


class ShelfItem(models.Model):
    datetime = models.DateField(auto_now_add=True)
    shelfRow = models.ForeignKey(ShelfRow,
                                 related_name='books',
                                 on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             related_name='row_items',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f"Item in Row {self.shelfRow.name} of {self.shelfRow.shelf.owner.username}"
