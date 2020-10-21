from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

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
    book_rate_form = BookRateForm()
    rating = BookRating.get_book_rating(request.user, book)

    return render(request, 'books/book_detail.html', {'book': book,
                                                      'section': 'search',
                                                      'book_rate_form': book_rate_form,
                                                      'rating': rating})


@require_POST
@login_required
def book_rate(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    try:
        rating = BookRating.objects.get(rated_by=request.user, book_rated=book)
        book_rate_form = BookRateForm(instance=rating, data=request.POST)
        prev_rating = rating.rate
    except BookRating.DoesNotExist:
        book_rate_form = BookRateForm(data=request.POST)
        rating = None

    # Update the rating value
    if book_rate_form.is_valid() and rating:
        # remove old rating from the average
        if book.num_ratings == 1:
            book.average_rating = 0
        else:
            book.update_rating_delete(prev_rating)

        rating = book_rate_form.save()
        # then add the new rating to average
        book.update_rating_add(rating.rate)
        book.save()

        messages.success(request, 'Rating updated successfully!')
    # Create new rating value
    elif book_rate_form.is_valid():
        rating = book_rate_form.save(commit=False)
        rating.rated_by = request.user
        rating.book_rated = book
        rating.save()

        # add new average_rating and num_ratings to book
        book.add_value_to_rating(rating.rate)
        book.save()

        messages.success(request, 'New rating added successfully!')
    return redirect(book)
