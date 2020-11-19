from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile
from ..forms import ProfileEditForm, UserEditForm, UserRegistrationForm


class ProfileEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='testing1234')
        self.profile = Profile.objects.create(user=self.user)

    def test_profile_form_saves_same_object(self):
        form = ProfileEditForm(instance=self.profile, data={'location': 'nowhere',
                                                            'date_of_birth': '1999-11-17'})
        new_profile = form.save()
        self.assertEquals(new_profile, self.profile)

    def test_profile_form_saves_changes(self):
        form = ProfileEditForm(instance=self.profile, data={'location': 'nowhere',
                                                            'date_of_birth': '1999-11-17'})
        new_profile = form.save()
        self.assertEquals(new_profile, Profile.objects.first())
        self.assertEquals(new_profile.location, 'nowhere')
        self.assertEquals(new_profile.date_of_birth.strftime('%Y-%m-%d'), '1999-11-17')


class UserEditFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='testing1234')

    def test_profile_form_saves_same_object(self):
        form = UserEditForm(instance=self.user, data={'first_name': 'Bogdan',
                                                      'last_name': 'Tudorache'})
        new_user = form.save()
        self.assertEquals(new_user, self.user)

    def test_user_form_saves_changes(self):
        form = UserEditForm(instance=self.user, data={'first_name': 'Bogdan',
                                                      'last_name': 'Tudorache'})
        new_user = form.save()
        self.assertEquals(new_user, User.objects.first())
        self.assertEquals(new_user.first_name, 'Bogdan')
        self.assertEquals(new_user.last_name, 'Tudorache')


class UserRegistrationFormTest(TestCase):
    def test_user_registration_form_saves_new_instance(self):
        form = UserRegistrationForm(data={'username': 'test_user',
                                          'email': 'test_user@mail.com',
                                          'password': 'testing1234',
                                          'password2': 'testing1234'})
        new_user = form.save(commit=False)
        # should not throw error
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()

        self.assertEquals(new_user, User.objects.first())
        self.assertEquals(new_user.username, 'test_user')
        self.assertEquals(new_user.email, 'test_user@mail.com')

    def test_user_registration_form_invalid_password(self):
        form = UserRegistrationForm(data={'username': 'test_user',
                                          'email': 'test_user@mail.com',
                                          'password': 'testing1234',
                                          'password2': 'testing4321'})

        self.assertFalse(form.is_valid())