from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import (
    Book,
    Genre,
    BookRating,
)
from .forms import BookRateForm, SearchForm


@login_required
def book_search_list(request, genre_id=None, author_id=None):
    search_form = SearchForm()
    if genre_id:
        books = Book.objects.filter(genre__id=genre_id)
    # Form variable 'query' is given to the request dictionary if the form on the website is submitted
    elif author_id:
        books = Book.objects.filter(author__id=author_id)
    elif 'query' in request.GET:
        search_form = SearchForm(data=request.GET)
        if search_form.is_valid():
            search_object = search_form.cleaned_data['query']
            words = search_object.split()
            # Search object must have more than 1 letter
            if len(search_object) == 1:
                books = None
            else:
                books = Book.objects.filter(Book.create_search_query(search_object.split()))
    else:
        search_form = SearchForm()
        books = Book.objects.all()
    genres = Genre.objects.all()
    return render(request, 'books/book_search_list.html', {'books': books,
                                                           'section': 'search',
                                                           'genres': genres,
                                                           'search_form': search_form})


@login_required
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
