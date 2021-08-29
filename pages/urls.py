from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('icon', views.icon_view, name='icon'),
    path('email-verify-done', views.email_verified_view, name='email_verify_done'),
    path('page/home', views.home_view, name='home'),
    path('page/jewellery-guide', views.jewellery_guide_view, name='jewellery_guide'),
    path('page/contact', views.contact_view, name='contact'),
    path('page/necklaces', views.necklaces_view, name='necklaces'),
    path('page/rings', views.rings_view, name='rings'),
    path('page/bracelets', views.bracelets_view, name='bracelets'),
    path('page/earrings', views.earrings_view, name='earrings'),
    path('page/about', views.about_view, name='about')
]