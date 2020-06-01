from django.contrib.auth.models import User
from django.db import models



class BlogUser(User):
    bio_info = models.TextField(help_text='Enter some biographical information.')
