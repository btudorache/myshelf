from django.contrib.auth.views import LoginView
from django.shortcuts import render

from .forms import (
    UserRegistrationForm,
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
            # Save the form but don't commmit the action
            new_user = user_form.save(commit=False)
            # Take care of the password hashing
            new_user.set_password(user_form.cleaned_data['password'])
            # Finally save the form
            new_user.save()
            return render(request, 'accounts/user/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'accounts/user/register.html', {'user_form': user_form, 'section': 'register'})
