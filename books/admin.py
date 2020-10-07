from django.contrib import admin
from .models import Genre, Author, Book, BookRating


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['genre']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ['rated_by', 'rate', 'book_rated']