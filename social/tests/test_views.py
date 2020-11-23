from django.test import TestCase
from django.contrib.auth.models import User

from ..models import Contact
from accounts.models import Profile


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')

    def test_template_used_when_not_logged(self):
        request = self.client.get('')
        self.assertTemplateUsed(request, 'social/home.html')

    def test_template_used_when_logged(self):
        self.client.login(username='test_user', password='testing1234')
        request = self.client.get('')
        self.assertTemplateUsed(request, 'social/dashboard.html')


class UserListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.client.login(username='test_user', password='testing1234')

    def test_view_uses_correct_template(self):
        request = self.client.get('/social/')
        self.assertTemplateUsed(request, 'social/user_list.html')

    def test_get_all_users(self):
        user1 = User.objects.create_user(username='test_user1', password='testing1234')
        user2 = User.objects.create_user(username='test_user2', password='testing1234')
        user3 = User.objects.create_user(username='test_user3', password='testing1234')

        request = self.client.get('/social/')
        request_users = request.context['users']
        self.assertEquals(len(list(request_users)), 3)

    def test_get_query_users(self):
        user1 = User.objects.create_user(username='abcde', password='testing1234')
        user2 = User.objects.create_user(username='abc', password='testing1234')
        user3 = User.objects.create_user(username='test_user3', password='testing1234')

        request = self.client.get('/social/', data={'query': 'abc'})
        request_users = request.context['users']
        self.assertEquals(len(list(request_users)), 2)

    def test_get_query_no_results(self):
        user1 = User.objects.create_user(username='test_user1', password='testing1234')
        user2 = User.objects.create_user(username='test_user2', password='testing1234')
        user3 = User.objects.create_user(username='test_user3', password='testing1234')

        request = self.client.get('/social/', data={'query': 'q'})
        request_users = request.context['users']
        self.assertEquals(len(list(request_users)), 0)


class UserDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='testing1234')
        self.profile = Profile.objects.create(user=self.user)
        self.client.login(username='test_user', password='testing1234')

    def test_view_uses_correct_template(self):
        request = self.client.get(f'/social/{self.user.id}/')
        self.assertTemplateUsed(request, 'social/user_detail.html')

    def test_detail_view_gets_correct_user(self):
        request = self.client.get(f'/social/{self.user.id}/')
        self.assertEquals(request.context['user'], self.user)
