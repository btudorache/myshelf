from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import SearchForm
from .models import Contact
from actions.models import Action
from actions.utils import create_action
from .utils import create_user_search_query


def dashboard(request):
    if request.user.is_authenticated:
        # Display all actions by default
        actions = Action.objects.exclude(user=request.user)
        following_ids = request.user.following.values_list('id', flat=True)

        if following_ids:
            # if user is following others, retrieve only their actions
            actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:20]

        return render(request, 'social/dashboard.html', {'section': 'home',
                                                         'actions': actions})
    else:
        # Else return homepage
        return render(request, 'social/home.html', {'section': 'home'})


@login_required
def user_list(request):
    if 'query' in request.GET and request.GET['query']:
        search_form = SearchForm(data=request.GET)
        if search_form.is_valid():
            search_object = search_form.cleaned_data['query']
            # Search object must have more than 1 letter
            if len(search_object) == 1:
                users = []
            else:
                users = User.objects.filter(create_user_search_query(search_object.split()))
                users = users.exclude(username=request.user.username)
    else:
        users = User.objects.exclude(username=request.user.username)[:25]
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


