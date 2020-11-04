from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .models import Contact
from actions.models import Action
from actions.utils import create_action


def home(request):
    return render(request, 'social/home.html', {'section': 'home'})


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)

    if following_ids:
        # if user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]

    return render(request, 'social/dashboard.html', {'section': 'dashboard',
                                                     'actions': actions})


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

        # Action for following new user
        create_action(request.user, 'started following', user)

    return redirect('social_user_detail', user_id=user_id)


