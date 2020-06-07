from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('bloguser/<int:pk>/', views.BlogUserDetailView.as_view(), name='bloguser-detail'),
    path('blogusers/', views.BlogUserListView.as_view(), name='bloggers'),
    path('blogs/', views.BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog'),
    path('comment/create/<int:blog_pk>/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment')
]
