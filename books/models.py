from django.db import models
from PIL import Image


class Genre(models.Model):
    genre = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.genre}'


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(default='default_book.jpg', upload_to='book_covers/')

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)

        img = Image.open(self.cover.path)

        if img.height != 350 or img.width != 233:
            output_size = (233, 350)
            img.thumbnail(output_size)
            img.save(self.cover.path)
