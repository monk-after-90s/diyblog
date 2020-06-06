from django.forms import ModelForm

from blog.models import BlogUser, Comment


class BlogUserModelForm(ModelForm):
    class Meta:
        model = BlogUser
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class CommentModelForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
