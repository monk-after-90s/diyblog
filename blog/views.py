from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView

from blog.forms import BlogUserModelForm
from blog.models import BlogUser, Blog, Comment


def index(request):
    return render(request, 'blog/index.html')


class BlogUserDetailView(ListView):
    model = Blog
    template_name = 'blog/bloguser_detail.html'

    def get_queryset(self):
        return Blog.objects.filter(author_id=int(self.kwargs['pk']))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['bloguser'] = BlogUser.objects.get(pk=int(self.kwargs['pk']))
        return context


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


class CommentDetailView(DetailView):
    model = Comment


# @login_required
# def comment_create_view(request, blog_pk: int):
#     blog = Blog.objects.get(pk=blog_pk)
#     if request.method == 'GET':
#         blog = Blog.objects.get(pk=blog_pk)
#         form = CommentModelForm()
#         context = {
#             'form': form,
#             'blog': blog
#         }
#         return render(request, 'blog/comment_form.html', context=context)
#     else:
#         form = CommentModelForm(request.POST)
#         if form.is_valid():
#             new_comment = Comment.objects.create(
#                 content=form.cleaned_data['content'],
#                 blog=blog,
#                 bloguser=BlogUser.objects.get(pk=(request.user.pk))
#             )
#             new_comment.save()
#         return HttpResponseRedirect(reverse('blog', args=(blog_pk,)))
class CommentCreateView(LoginRequiredMixin, CreateView):
    fields = ['content']
    model = Comment

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(pk=int(self.kwargs['blog_pk']))
        return context

    def form_valid(self, form):
        form.instance.bloguser = BlogUser.objects.get(pk=int(self.request.user.pk))
        form.instance.blog = get_object_or_404(Blog, pk=int(self.kwargs['blog_pk']))
        return super(CommentCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog', args=(str(self.kwargs['blog_pk']),))
