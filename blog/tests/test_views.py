from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from blog.models import BlogUser


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


class LogoutViewTest(TestCase):
    def setUp(self) -> None:
        testuser = User.objects.create_user(username='testuser', password='bdakfkweqhfewfbds')
        testuser.save()
        login_res = self.client.login(username='testuser', password='bdakfkweqhfewfbds')
        self.assertEqual(login_res, True)

    def test_user_logged_out(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'AnonymousUser')


class RegisterViewTest(TestCase):
    def test_register_then_redirect2bloguser_detail(self):
        response = self.client.post(reverse('register'),
                                    data={'username': 'testuser',
                                          'password': 'tyhnyru65654hre3twgaregq3',
                                          'first_name': 'test_first_name',
                                          'last_name': 'test_last_name',
                                          'email': 'abc@def.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('bloguser-detail', kwargs={'pk': 1}))

    def test_registration_creates_bloguser(self):
        response = self.client.post(reverse('register'),
                                    data={'username': 'testuser',
                                          'password': 'tyhnyru65654hre3twgaregq3',
                                          'first_name': 'test_first_name',
                                          'last_name': 'test_last_name',
                                          'email': 'abc@def.com'})

        self.assertEqual(response.status_code, 302)
        new_user = BlogUser.objects.get(pk=1)
        self.assertEqual(new_user.username, 'testuser')
        self.assertEqual(new_user.first_name, 'test_first_name')
        self.assertEqual(new_user.last_name, 'test_last_name')
        self.assertEqual(new_user.email, 'abc@def.com')

    def test_register_then_login(self):
        response = self.client.post(reverse('register'),
                                    data={'username': 'testuser',
                                          'password': 'tyhnyru65654hre3twgaregq3',
                                          'first_name': 'test_first_name',
                                          'last_name': 'test_last_name',
                                          'email': 'abc@def.com'})
        self.client.login(username='testuser',
                          password='tyhnyru65654hre3twgaregq3')
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(str(response.context['user']), 'testuser')
