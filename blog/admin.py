from django.contrib import admin

# Register your models here.
from blog.models import BlogUser, Blog, Comment

admin.site.register(Comment)


class BlogInline(admin.TabularInline):
    model = Blog
    extra = 0


@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'bio_info']
    # fields = ['username', ('email', 'bio_info')]
    fieldsets = (
        ('称谓', {'fields': ('username',)}),
        ('详情', {'fields': ('email', 'bio_info')})
    )
    inlines = [BlogInline]


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    list_display = ['name', 'author', 'post_date', 'content']
