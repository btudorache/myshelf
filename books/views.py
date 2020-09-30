from django.shortcuts import render

from .models import Book


def book_search_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_search_list.html', {'books': books, 'section': 'search'})
