from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('customer', views.customer_dashboard_view, name='customer_dashboard'),
    # path('customers-json/<int:num_cust>/', views.customers_json, name='customers_json'),
    path('customer/<int:id>', views.customer_detail_dashboard_view, name='customer_detail_dashboard'),
    path('orders', views.order_dashboard_view, name='order_dashboard'),
]