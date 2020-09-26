from django.shortcuts import render


def home(request):
    return render(request, 'layout/home.html', {'section': 'home'})
