from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import (
    Book,
    Genre,
    BookRating,
)
from .forms import BookRateForm


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
    # view for both adding a new rating or updating and old one
    book = get_object_or_404(Book, id=book_id)
    try:
        rating = BookRating.objects.get(rated_by=request.user, book_rated=book)
    except BookRating.DoesNotExist:
        rating = None

    if request.method == 'POST':
        if rating:
            book_rate_form = BookRateForm(instance=rating, data=request.POST)
        else:
            book_rate_form = BookRateForm(data=request.POST)

        if book_rate_form.is_valid() and rating:
            rating = book_rate_form.save()
            messages.success(request, 'Rating updated successfully!')
        elif book_rate_form.is_valid():
            rating = book_rate_form.save(commit=False)
            rating.rated_by = request.user
            rating.book_rated = book
            rating.save()
            messages.success(request, 'New rating added successfully!')
    else:
        book_rate_form = BookRateForm()
    return render(request, 'books/book_detail.html', {'book': book,
                                                      'section': 'search',
                                                      'book_rate_form': book_rate_form,
                                                      'rating': rating})
