from django.shortcuts import render


def shelf_lists(request):
    return render(request, 'shelf/shelf_lists.html', {'section': 'shelf'})
