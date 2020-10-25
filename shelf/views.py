from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render, redirect

from books.models import Book
from .models import Shelf, ShelfRow, ShelfItem

from .forms import ShelfItemForm


@login_required
def shelf_lists(request):
    shelf_rows = Shelf.objects.get(owner=request.user).get_shelves()
    return render(request, 'shelf/shelf_lists.html', {'section': 'shelf',
                                                      'shelf_rows': shelf_rows})


@login_required
@require_POST
def add_shelf_item(request, book_id):
    shelf_item_form = ShelfItemForm(user=request.user, data=request.POST)
    if shelf_item_form.is_valid():
        shelf_item_form.cleaned_data['shelf_row'].shelf_item_add()
        shelf_item = shelf_item_form.save(commit=False)

        book = Book.objects.get(id=book_id)
        shelf_item.book = book
        shelf_item.owner = request.user
        shelf_item.save()

        messages.success(request, "Book added to shelf successfully!")
        return redirect(book)


@login_required
@require_POST
def update_shelf_item(request, book_id, old_shelf_item_id):
    shelf_item_form = ShelfItemForm(user=request.user, data=request.POST)
    if shelf_item_form.is_valid():
        old_shelf_item = ShelfItem.objects.get(id=old_shelf_item_id)

        # When updating, update num_row only if shelves are different
        if old_shelf_item.shelf_row != shelf_item_form.cleaned_data['shelf_row']:
            old_shelf_item.shelf_row.shelf_item_delete()
        old_shelf_item.delete()

        # When updating, update num_row only if shelves are different
        if old_shelf_item.shelf_row != shelf_item_form.cleaned_data['shelf_row']:
            shelf_item_form.cleaned_data['shelf_row'].shelf_item_add()
        shelf_item = shelf_item_form.save(commit=False)

        book = Book.objects.get(id=book_id)
        shelf_item.book = book
        shelf_item.owner = request.user
        shelf_item.save()

        messages.success(request, "Book row updated successfully!")
        return redirect(book)

