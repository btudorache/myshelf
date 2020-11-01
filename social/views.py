from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Contact


def home(request):
    return render(request, 'social/home.html', {'section': 'home'})


@login_required
def user_list(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, 'social/user_list.html', {'section': 'social',
                                                     'users': users,})


@login_required
def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    contact = Contact.get_contact(request.user, user)
    return render(request, 'social/user_detail.html', {'section': 'social',
                                                       'contact': contact,
                                                       'user': user,})


@login_required
def user_follow(request, user_id, contact_id=None):
    if contact_id:
        Contact.objects.get(id=contact_id).delete()
    else:
        user = get_object_or_404(User, id=user_id)
        Contact.objects.create(user_from=request.user, user_to=user)
    return redirect('social_user_detail', user_id=user_id)


