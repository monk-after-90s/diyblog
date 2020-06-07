from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.urls import reverse

from blog.models import BlogUser, Blog


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


class BlogListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = BlogUser.objects.create_user(username='testbloguser',
                                              first_name='test',
                                              last_name='bloguser',
                                              password='dflewqlr23ru23u3423ryqe9fyq348g',
                                              email='nkdwkfda@qnewfnaf.com',
                                              bio_info='测试用的博客作者')
        author.save()
        for i in range(21):
            Blog.objects.create(
                author=author,
                content=f'这是一个测试用的博客{i}',
                name=f'测试博客{i}'
            ).save()

    def test_blog_list_view_is_accessible_at_the_expected_location(self):
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_blog_list_view_accessible_at_the_expected_named_url(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)

    def test_blog_list_view_uses_the_expected_template(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blog_list.html')

    def test_blog_list_view_paginates_records_by_5(self):
        response = self.client.get(reverse('blogs'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['object_list']), 5)

    def test_blog_list_view_lists_all_objects(self):
        response = self.client.get(reverse('blogs') + '?page=5')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['object_list']), 1)


class BlogDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = BlogUser.objects.create_user(username='testbloguser',
                                              first_name='test',
                                              last_name='bloguser',
                                              password='dflewqlr23ru23u3423ryqe9fyq348g',
                                              email='nkdwkfda@qnewfnaf.com',
                                              bio_info='测试用的博客作者')
        author.save()
        Blog.objects.create(
            author=author,
            content=f'这是一个测试用的博客',
            name=f'测试博客'
        ).save()

    def test_blog_detail_view_context(self):
        response = self.client.get(reverse('blog', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('blog' in response.context)

    def test_blog_detail_view_use_expected_template(self):
        response = self.client.get(reverse('blog', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blog_detail.html')

    def test_blog_detail_view_is_accessable_at_expected_url(self):
        response = self.client.get('/blog/blog/1/')
        self.assertEqual(response.status_code, 200)

    def test_blog_detail_view_is_accessable_at_expected_name(self):
        response = self.client.get(reverse('blog', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


class BloggerListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(17):
            author = BlogUser.objects.create_user(username=f'testbloguser{i}',
                                                  first_name=f'test{i}',
                                                  last_name=f'bloguser{i}',
                                                  password='dflewqlr23ru23u3423ryqe9fyq348g',
                                                  email='nkdwkfda@qnewfnaf.com',
                                                  bio_info=f'测试用的博客作者{i}')
            author.save()
            if i < 10:
                Blog.objects.create(
                    author=author,
                    content=f'这是一个测试用的博客',
                    name=f'测试博客'
                ).save()

    def test_blogger_list_view_accessable_at_expected_url(self):
        response = self.client.get('/blog/bloggers/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bloguser_list' in response.context)
        self.assertEqual(len(response.context['object_list']), 10)

    def test_blogger_list_view_accessable_at_expected_name(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('bloguser_list' in response.context)
        self.assertEqual(len(response.context['object_list']), 10)

    def test_blogger_list_vew_use_expected_template(self):
        response = self.client.get(reverse('bloggers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/blogger_list.html')


class CommentCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = BlogUser.objects.create_user(username='testbloguser',
                                              first_name='test',
                                              last_name='bloguser',
                                              password='dflewqlr23ru23u3423ryqe9fyq348g',
                                              email='nkdwkfda@qnewfnaf.com',
                                              bio_info='测试用的博客作者')
        author.save()
        Blog.objects.create(
            author=author,
            content=f'这是一个测试用的博客',
            name=f'测试博客'
        ).save()
        normal_bloguser = BlogUser.objects.create_user(username='normal_bloguser',
                                                       first_name='normal',
                                                       last_name='bloguser',
                                                       password='dflewqlr23ru23u3423ryqe9fyq348g',
                                                       email='nkdwkfda@qnewfnaf.com',
                                                       bio_info='测试用的博客评论者')
        normal_bloguser.save()

    def test_create_comment_when_not_login(self):
        response = self.client.get(reverse('comment-create', kwargs={'blog_pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login') + f"?next={reverse('comment-create', kwargs={'blog_pk': 1})}")

    def test_get_create_comment_when_login(self):
        login = self.client.login(username='normal_bloguser', password='dflewqlr23ru23u3423ryqe9fyq348g')
        response = self.client.get(reverse('comment-create', kwargs={'blog_pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_post_create_comment_when_login(self):
        login = self.client.login(username='normal_bloguser', password='dflewqlr23ru23u3423ryqe9fyq348g')
        response = self.client.post(reverse('comment-create', kwargs={'blog_pk': 1}),
                                    data={'blog': Blog.objects.get(pk=1),
                                          'bloguser': BlogUser.objects.get(pk=2),
                                          'content': '测试评论'})
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('blog/blog_detail.html')
        self.assertEqual(response.url, reverse('blog', args=(1,)))
