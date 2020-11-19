from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import UserRegistrationForm
from ..models import Profile
from shelf.models import Shelf


class RegisterPageTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/accounts/register/')
        self.user_data = {'username': 'test_user',
                          'email': 'test_user@mail.com',
                          'password': 'testing1234',
                          'password2': 'testing1234'}

    def test_register_template(self):
        self.assertTemplateUsed(self.response, 'accounts/register.html')

    def test_register_page_uses_registration_form(self):
        self.assertIsInstance(self.response.context['user_form'], UserRegistrationForm)

    def test_register_page_category(self):
        self.assertEquals(self.response.context['section'], 'register')

    def test_register_page_post_redirects_profile(self):
        response = self.client.post('/accounts/register/', self.user_data)
        self.assertTemplateUsed(response, 'accounts/register_done.html')

    def test_register_page_post_creates_user(self):
        self.client.post('/accounts/register/', self.user_data)
        new_user = User.objects.get(username='test_user')
        self.assertEquals(new_user, User.objects.first())

    def test_register_page_post_creates_profile(self):
        self.client.post('/accounts/register/', self.user_data)
        new_user = User.objects.get(username='test_user')
        profile = Profile.objects.get(user=new_user)
        self.assertEquals(profile, Profile.objects.first())

    def test_register_page_post_creates_shelf(self):
        self.client.post('/accounts/register/', self.user_data)
        new_user = User.objects.get(username='test_user')
        shelf = Shelf.objects.get(owner=new_user)
        self.assertEquals(shelf, Shelf.objects.first())


class LoginPageTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/accounts/login/')

    def test_login_template(self):
        self.assertTemplateUsed(self.response, 'registration/login.html')

    def test_register_page_category(self):
        self.assertEquals(self.response.context['section'], 'login')
