from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_redirect2blog(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 301)
        self.assertEqual('/' + response.url, reverse('index'))


class LoginViewTest(TestCase):
    def setUp(self) -> None:
        testuser = User.objects.create_user(username='testuser', password='bdakfkweqhfewfbds')
        testuser.save()

    def test_index_logged_in(self):
        login_res = self.client.login(username='testuser', password='bdakfkweqhfewfbds')
        self.assertEqual(login_res, True)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser')
