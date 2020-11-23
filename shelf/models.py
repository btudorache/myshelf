from django.conf import settings
from django.urls import reverse
from django.db import models

from books.models import Book


class Shelf(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 related_name='user_shelf',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.owner.username}'s shelf"

    def get_absolute_url(self):
        return reverse('shelf_lists', args=[self.owner.id])

    def get_shelves(self):
        return ShelfRow.objects.filter(shelf=self)

    @staticmethod
    def add_new_user_shelf(new_user):
        new_shelf = Shelf.objects.create(owner=new_user)
        ShelfRow.objects.create(owner=new_user, name="Read", shelf=new_shelf)
        ShelfRow.objects.create(owner=new_user, name="Currently Reading", shelf=new_shelf)
        ShelfRow.objects.create(owner=new_user, name="Want to Read", shelf=new_shelf)


class ShelfRow(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='user_shelf_row',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    shelf = models.ForeignKey(Shelf,
                              related_name='row',
                              on_delete=models.CASCADE)
    num_items = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('shelf_row_items', args=[self.id])

    def get_items(self):
        return ShelfItem.objects.filter(shelf_row=self)

    def shelf_item_add(self):
        self.num_items += 1
        self.save()

    def shelf_item_delete(self):
        self.num_items -= 1
        self.save()

    def __str__(self):
        return f"{self.name}"


class ShelfItem(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='user_shelf_row_item',
                              on_delete=models.CASCADE)
    datetime = models.DateField(auto_now_add=True)
    shelf_row = models.ForeignKey(ShelfRow,
                                  related_name='books',
                                  on_delete=models.CASCADE)
    book = models.ForeignKey(Book,
                             related_name='row_items',
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    @staticmethod
    def get_shelf_item(owner, book):
        try:
            shelf_item = ShelfItem.objects.get(owner=owner, book=book)
        except ShelfItem.DoesNotExist:
            shelf_item = None
        return shelf_item

    def __str__(self):
        return f"Item in Row {self.shelf_row.name} of {self.shelf_row.shelf.owner.username}"
