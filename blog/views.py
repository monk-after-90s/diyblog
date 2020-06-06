from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView, ListView

from blog.forms import BlogUserModelForm, CommentModelForm
from blog.models import BlogUser, Blog, Comment


def index(request):
    return render(request, 'blog/index.html')


class BlogUserDetailView(DetailView):
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


class BlogListView(ListView):
    model = Blog
    paginate_by = 5


class BlogUserListView(ListView):
    model = BlogUser

    def get_queryset(self):
        return BlogUser.objects.filter(blog__id__gt=0)


class BlogDetailView(DetailView):
    model = Blog


@login_required
def comment_create_view(request, blog_pk: int):
    blog = Blog.objects.get(pk=blog_pk)
    if request.method == 'GET':
        blog = Blog.objects.get(pk=blog_pk)
        form = CommentModelForm()
        context = {
            'form': form,
            'blog': blog
        }
        return render(request, 'blog/comment_form.html', context=context)
    else:
        form = CommentModelForm(request.POST)
        if form.is_valid():
            new_comment = Comment.objects.create(
                content=form.cleaned_data['content'],
                blog=blog,
                bloguser=BlogUser.objects.get(pk=(request.user.pk))
            )
            new_comment.save()
        return HttpResponseRedirect(reverse('blog', args=(blog_pk,)))
