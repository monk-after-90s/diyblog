from django.test import TestCase

from blog.models import Blog, BlogUser


class BlogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = BlogUser(username='testbloguser',
                          first_name='test',
                          last_name='bloguser',
                          password='dflewqlr23ru23u3423ryqe9fyq348g',
                          email='nkdwkfda@qnewfnaf.com',
                          bio_info='测试用的博客作者')
        author.save()
        Blog.objects.create(
            author=author,
            content='这是一个测试用的博客',
            name='测试博客'
        ).save()

    def test_get_absolute_url(self):
        blog = Blog.objects.get(pk=1)
        self.assertEqual(blog.get_absolute_url(), '/blog/blog/1/')

    def test_field_label(self):
        blog = Blog.objects.get(pk=1)
        self.assertEqual(blog._meta.get_field('name').verbose_name, 'name')
        self.assertEqual(blog._meta.get_field('author').verbose_name, 'author')
        self.assertEqual(blog._meta.get_field('post_date').verbose_name, 'post date')
        self.assertEqual(blog._meta.get_field('content').verbose_name, 'content')

    def test_field_length(self):
        blog = Blog.objects.get(pk=1)
        self.assertEqual(blog._meta.get_field('name').max_length, 50)
        self.assertEqual(blog._meta.get_field('content').max_length, 5000)

    def test_object_name_is_name_peoperty(self):
        blog = Blog.objects.get(pk=1)
        self.assertEqual(str(blog), blog.name)

    def test_blog_author_is_bloguser(self):
        blog = Blog.objects.get(pk=1)
        self.assertEqual(blog.author, BlogUser.objects.get(pk=1))
