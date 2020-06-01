from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.views.generic import CreateView

from blog.models import Blog, BlogUser


def index(request):
    return render(request, 'blog/index.html')


class RegisterView(CreateView):
    model = BlogUser
    fields = ['username', 'password', 'first_name', 'last_name', 'email']
