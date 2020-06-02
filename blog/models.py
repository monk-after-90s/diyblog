from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class BlogUser(User):
    bio_info = models.TextField(null=True, blank=True, help_text='Enter some biographical information.')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('bloguser-detail', args=[str(self.id)])
