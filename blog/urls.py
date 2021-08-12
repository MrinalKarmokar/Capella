from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_home_view, name='blog'),
    path('<int:id>', views.blog_view, name='blog_post'),
]