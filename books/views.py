from django.shortcuts import render

from .models import Book, Genre


def book_search_list(request, genre_id=None):
    if genre_id is None:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(genre__id=genre_id)
    genres = Genre.objects.all()
    return render(request, 'books/book_search_list.html', {'books': books,
                                                           'section': 'search',
                                                           'genres': genres})
