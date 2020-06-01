from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.views.generic import CreateView, DetailView

from blog.models import BlogUser


def index(request):
    return render(request, 'blog/index.html')


class BlogAuthorDetailView(DetailView):
    model = BlogUser
    fields = ['username', 'password', 'first_name', 'last_name', 'email']


class BlogUserCreateView(CreateView):
    model = BlogUser
    fields = ['username', 'password', 'first_name', 'last_name', 'email']
