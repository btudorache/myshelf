from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Profile
from shelf.models import Shelf, ShelfRow

from .forms import (
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm,
)


# Extended LoginView to add section to context
class CustomLoginView(LoginView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['section'] = 'login'
        return context


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Save the form but don't commit the action
            new_user = user_form.save(commit=False)
            # Take care of the password hashing
            new_user.set_password(user_form.cleaned_data['password'])
            # Finally save the form
            new_user.save()

            # Create profile for the new user
            Profile.objects.create(user=new_user)

            # Add initial shelf + shelf rows
            Shelf.add_new_user_shelf(new_user)
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'user_form': user_form, 'section': 'register'})


@login_required
def user_detail(request):
    user = get_object_or_404(User, username=request.user.username, is_active=True)
    return render(request, 'accounts/user/user_detail.html', {'section': 'profile', 'user': user})


@login_required
def update_user(request):
    if request.method == 'POST':
        user_update_form = UserEditForm(instance=request.user, data=request.POST)
        profile_update_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, 'Profile updated successfully')

            return redirect(request.user.profile)
    else:
        user_update_form = UserEditForm(instance=request.user)
        profile_update_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'accounts/user/user_update.html', {'user_form': user_update_form,
                                                              'profile_form': profile_update_form,
                                                              'section': 'profile'})
