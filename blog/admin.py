from django.contrib import admin

# Register your models here.
from blog.models import BlogUser, Blog


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
