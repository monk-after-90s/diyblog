from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=50, help_text='Enter the name of the blog.')
    author = models.ForeignKey('BlogUser', on_delete=models.SET_NULL, null=True)
    post_date = models.DateField(auto_now_add=True)
    content = models.TextField(max_length=5000, help_text='Type your blog.')

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.name


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_datetime = models.DateTimeField(auto_now_add=True)
    bloguser = models.ForeignKey('BlogUser', on_delete=models.SET_NULL, null=True)
    content = models.TextField(max_length=200, help_text='键入对该博客的评论')

    class Meta:
        ordering = ['post_datetime']

    def __str__(self):
        return f'{self.bloguser}({self.post_datetime}) - {self.content[:75]}'


class BlogUser(User):
    bio_info = models.TextField(max_length=200, null=True, blank=True, help_text='Enter some biographical information.')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('bloguser-detail', args=[str(self.id)])
