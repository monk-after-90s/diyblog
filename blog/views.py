from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView

from blog.forms import BlogUserModelForm
from blog.models import BlogUser


def index(request):
    return render(request, 'blog/index.html')


class BlogAuthorDetailView(DetailView):
    model = BlogUser


def register_view(request):
    if request.method == 'GET':
        form = BlogUserModelForm()
    else:
        form = BlogUserModelForm(request.POST)
        if form.is_valid():
            new_blog_user = BlogUser.objects.create_user(
                **{key: request.POST[key] for key in BlogUserModelForm.Meta.fields})
            new_blog_user.save()
            return HttpResponseRedirect(reverse('bloguser-detail', args=[str(new_blog_user.pk)]))

    context = {
        'form': form
    }
    return render(request, 'blog/bloguser_form.html', context=context)
