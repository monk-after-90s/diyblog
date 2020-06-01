from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('bloguser/<int:pk>/', views.BlogAuthorDetailView.as_view(), name='bloguser-detail'),
    path('register/', views.BlogUserCreateView.as_view(), name='register')
]
