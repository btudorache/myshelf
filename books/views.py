from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from actions.utils import create_action

from .models import (
    Book,
    Genre,
    BookRating,
    BookReview,
)
from shelf.models import ShelfItem, Shelf

from .forms import BookRateForm, SearchForm, BookReviewForm
from shelf.forms import ShelfItemForm


@login_required
def book_search_list(request, genre_id=None, author_id=None):
    search_form = SearchForm()
    if genre_id:
        books = Book.objects.filter(genre__id=genre_id)
    # Form variable 'query' is given to the request dictionary if the form on the website is submitted
    elif author_id:
        books = Book.objects.filter(author__id=author_id)
    elif 'query' in request.GET and request.GET['query']:
        search_form = SearchForm(data=request.GET)
        if search_form.is_valid():
            search_object = search_form.cleaned_data['query']
            # Search object must have more than 1 letter
            if len(search_object) == 1:
                books = []
            else:
                books = Book.objects.filter(Book.create_search_query(search_object.split()))
    else:
        books = Book.objects.all()
    genres = Genre.objects.all()

    paginator = Paginator(books, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/book_search_list.html', {'section': 'search',
                                                           'genres': genres,
                                                           'search_form': search_form,
                                                           'page_obj': page_obj})


@login_required
def book_detail(request, book_id):
    # view for both adding a new rating or updating and old one
    book = get_object_or_404(Book, id=book_id)
    book_rate_form = BookRateForm()
    shelf_item_form = ShelfItemForm(user=request.user)
    shelf_item = ShelfItem.get_shelf_item(request.user, book)
    rating = BookRating.get_book_rating(request.user, book)
    review = BookReview.get_book_review(request.user, book)
    reviews = BookReview.objects.filter(book_reviewed=book)

    paginator = Paginator(reviews, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/book_detail.html', {'book': book,
                                                      'shelf_item':shelf_item,
                                                      'section': 'search',
                                                      'book_rate_form': book_rate_form,
                                                      'shelf_item_form': shelf_item_form,
                                                      'rating': rating,
                                                      'review': review,
                                                      'page_obj': page_obj})


@require_POST
@login_required
def book_rate_create(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book_rate_form = BookRateForm(data=request.POST)

    if book_rate_form.is_valid():
        rating = book_rate_form.save(commit=False)
        rating.rated_by = request.user
        rating.book_rated = book
        rating.save()

        # add new average_rating and num_ratings to book
        book.add_value_to_rating(rating.rate)
        book.save()

        # Create new book_rate action
        create_action(request.user, 'rated', book)

        messages.success(request, 'New rating added successfully!')
    return redirect(book)


@require_POST
@login_required
def book_rate_update(request, book_id, rating_id):
    rating = BookRating.objects.get(id=rating_id)
    book = Book.objects.get(id=book_id)
    prev_rating = rating.rate
    book_rate_form = BookRateForm(instance=rating, data=request.POST)

    if book_rate_form.is_valid():
        if book.num_ratings == 1:
            book.average_rating = 0
        else:
            book.update_rating_delete(prev_rating)

        rating = book_rate_form.save()
        # then add the new rating to average
        book.update_rating_add(rating.rate)
        book.save()

        messages.success(request, 'Rating updated successfully!')
    return redirect(book)


@login_required
def book_create_review(request, book_title):
    if request.method == 'POST':
        book_review_form = BookReviewForm(data=request.POST)
        if book_review_form.is_valid():
            review = book_review_form.save(commit=False)

            book = Book.objects.get(title=book_title)
            review.book_reviewed = book
            review.reviewer = request.user
            review.save()

            # Create new review
            create_action(request.user, 'reviewed book', review)

            messages.success(request, "Review added successfully!")
            return redirect(book)
    else:
        book_review_form = BookReviewForm()
        return render(request, 'books/book_create_review.html', {'section': 'search',
                                                                 'book_review_form': book_review_form})


@login_required
def book_update_review(request, book_title, review_id):
    review = BookReview.objects.get(id=review_id)
    if request.method == 'POST':
        book_review_form = BookReviewForm(data=request.POST, instance=review)
        if book_review_form.is_valid():
            book_review_form.save()
            book = Book.objects.get(title=book_title)

            messages.success(request, "Review updated successfully!")
            return redirect(book)
    else:
        book_review_form = BookReviewForm(instance=review)
        return render(request, 'books/book_update_review.html', {'section': 'search',
                                                                 'book_review_form': book_review_form})

