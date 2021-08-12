from django.urls import path
from . import views

urlpatterns = [
    path('place-order', views.place_order_view, name='place_order'),
    path('your-orders', views.your_order_view, name='your_orders')
]