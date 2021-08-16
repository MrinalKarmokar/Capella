from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('icon', views.icon_view, name='icon'),
    path('email-verify-done', views.email_verified_view, name='email_verify_done'),
    path('page/home', views.home_view, name='home'),
    path('page/contact', views.contact_view, name='contact'),
    path('page/necklaces', views.necklaces_view, name='necklaces'),
    path('page/rings', views.rings_view, name='rings'),
    path('page/bracelets', views.bracelets_view, name='bracelets'),
    path('page/earrings', views.earrings_view, name='earrings'),
]