from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test_user1', password='testing1234')
        self.user2 = User.objects.create_user(username='test_user2', password='testing1234')

    def test_create_contact_model_instance(self):
        contact = Contact.objects.create(user_from=self.user1, user_to=self.user2)
        self.assertEquals(contact, Contact.objects.first())

    def test_get_contact_method_1(self):
        contact = Contact.objects.create(user_from=self.user1, user_to=self.user2)
        self.assertEquals(contact, Contact.get_contact(self.user1, self.user2))

    def test_get_contact_method_2(self):
        self.assertTrue(Contact.get_contact(self.user1, self.user2) is None)


class UserModelFollowingFieldTest(TestCase):
    def test_user_following_field_added(self):
        self.assertTrue(User.following is not None)