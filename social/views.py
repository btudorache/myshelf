from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404


def home(request):
    return render(request, 'social/home.html', {'section': 'home'})


def user_list(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'social/user_list.html', {'section': 'social',
                                                     'users': users,})


def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'social/user_detail.html', {'section': 'social',
                                                       'user': user,})