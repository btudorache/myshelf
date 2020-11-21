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


class UserDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='test_user', password='testing1234')
        self.response = self.client.get('/accounts/profile/')

    def test_user_detail_page_template(self):
        self.assertTemplateUsed(self.response, 'accounts/user/user_detail.html')

    def test_user_detail_page_gets_correct_user(self):
        self.assertContains(self.response, self.user.username)


class UserUpdateProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='test_user', password='testing1234')

    def test_get_request_status_code(self):
        response = self.client.get('/accounts/profile/update/')
        self.assertEquals(response.status_code, 200)

    def test_get_response_template(self):
        response = self.client.get('/accounts/profile/update/')
        self.assertTemplateUsed(response, 'accounts/user/user_update.html')

    def test_correct_redirect_after_post_request(self):
        response = self.client.post('/accounts/profile/update/', {'first_name': 'Bogdan',
                                                                  'last_name': 'Tudorache',
                                                                  'location': 'Focsani',
                                                                  'date_of_birth': '1999-11-17'})
        self.assertEquals(response.url, '/accounts/profile/')
