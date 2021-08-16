from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_home_view, name='payment_home'),
    # path('<int:id>', views.blog_view, name='blog_post'),
]