from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user', password='testing1234')
        self.profile = Profile.objects.create(user=self.user)

    def test_default_profile_created(self):
        self.assertEquals(Profile.objects.first(), self.profile)

    def test_user_has_correct_profile(self):
        self.assertEquals(self.user.profile, self.profile)

    def test_profile_default_image(self):
        self.assertEquals(self.profile.photo.name, 'default_profile.jpg')

    def test_profile_get_absolute_url(self):
        self.assertEquals(self.profile.get_absolute_url(), '/accounts/profile/')

    def test_custom_profile_created(self):
        new_user = User.objects.create_user('test_user2', password='testing1234')
        new_profile = Profile.objects.create(user=new_user, location='nowhere', date_of_birth='1999-11-17')
        self.assertEquals(new_profile.location, 'nowhere')
        self.assertEquals(new_profile.date_of_birth, '1999-11-17')
