from django.test import TestCase
from django.contrib.auth.models import User

from ..forms import UserRegistrationForm


class RegisterPageTest(TestCase):
    def test_register_template(self):
        response = self.client.get('/accounts/register/')
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_page_uses_registration_form(self):
        response = self.client.get('/accounts/register/')
        self.assertIsInstance(response.context['user_form'], UserRegistrationForm)