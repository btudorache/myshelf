from django.shortcuts import render, get_object_or_404

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


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'books/book_detail.html', {'book': book, 'section': 'book_detail'})
