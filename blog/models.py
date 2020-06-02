from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.
class Blog(models.Model):
    name = models.CharField(max_length=50, help_text='Enter the name of the blog.')
    author = models.ForeignKey('BlogUser', on_delete=models.SET_NULL, null=True)
    post_date = models.DateField(auto_now_add=True)
    content = models.TextField(help_text='Type your blog.')

    class Meta:
        ordering = ['-post_date']


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    bloguser = models.ForeignKey('BlogUser', on_delete=models.SET_NULL, null=True)


class BlogUser(User):
    bio_info = models.TextField(null=True, blank=True, help_text='Enter some biographical information.')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('bloguser-detail', args=[str(self.id)])
