from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=50)
    description = models.TextField()


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    description = models.TextField()
