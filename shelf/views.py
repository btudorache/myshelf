from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Shelf, ShelfRow


@login_required
def shelf_lists(request):
    shelf_rows = Shelf.objects.get(owner=request.user).get_shelves()
    return render(request, 'shelf/shelf_lists.html', {'section': 'shelf',
                                                      'shelf_rows': shelf_rows})
