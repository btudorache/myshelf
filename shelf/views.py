from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render, redirect

from actions.utils import create_action
from books.models import Book
from .models import Shelf, ShelfRow, ShelfItem

from .forms import ShelfItemForm, ShelfRowForm


@login_required
def shelf_lists(request):
    shelf_rows = Shelf.objects.get(owner=request.user).get_shelves()
    return render(request, 'shelf/shelf_lists.html', {'section': 'shelf',
                                                      'shelf_rows': shelf_rows})


@login_required
def shelf_row_items(request, shelf_row_id):
    row = ShelfRow.objects.get(id=shelf_row_id)
    row_items = row.get_items()

    paginator = Paginator(row_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shelf/shelf_row_items.html', {'section': 'shelf',
                                                          'row': row,
                                                          'page_obj': page_obj})


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

        # Create new book_rate action
        create_action(request.user, 'added book to shelf', shelf_item_form.cleaned_data['shelf_row'])

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


@login_required
def delete_shelf_item(request, shelf_item_id, section):
    shelf_item = ShelfItem.objects.get(id=shelf_item_id)
    shelf_item.shelf_row.shelf_item_delete()
    if section == 'search':
        book = Book.objects.get(id=shelf_item.book.id)
        shelf_item.delete()
        return redirect(book)
    elif section == 'shelf':
        shelf_row = ShelfRow.objects.get(id=shelf_item.shelf_row.id)
        shelf_item.delete()
        return redirect(shelf_row)


@login_required
def add_shelf(request):
    if request.method == 'POST':
        shelf_row_form = ShelfRowForm(data=request.POST)
        if shelf_row_form.is_valid():
            shelf_row = shelf_row_form.save(commit=False)
            shelf_row.owner = request.user
            shelf_row.shelf = request.user.user_shelf
            shelf_row.is_default = True
            shelf_row.save()

            messages.success(request, "New Shelf Row Added Successfully!")
            return redirect(request.user.user_shelf)
    else:
        shelf_row_form = ShelfRowForm()
        return render(request, 'shelf/shelf_row_add.html', {'section': 'shelf',
                                                            'shelf_row_form': shelf_row_form})


@login_required
def delete_shelf_row(request, shelf_row_id):
    shelf_row = ShelfRow.objects.get(id=shelf_row_id)
    shelf_row.delete()
    return redirect(request.user.user_shelf)