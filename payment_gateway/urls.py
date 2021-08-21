from django.urls import path
from . import views

urlpatterns = [
    path('pay', views.payment_home_view, name='payment_home'),
    path('success', views.payment_success_view, name='payment_success'),
]