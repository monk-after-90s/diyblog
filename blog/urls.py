from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('bloguser/<int:pk>/', views.BlogUserDetailView.as_view(), name='bloguser-detail'),
    path('blogusers/', views.BlogUserListView.as_view(), name='bloggers')
]
