from django.shortcuts import render


def home(request):
    return render(request, 'social/home.html', {'section': 'home'})