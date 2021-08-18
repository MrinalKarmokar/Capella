# from django.db.models.expressions import F
from django.core import paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator

from accounts.models import Account, AccountExtention, UserAddress
from order.models import ornamentOrder

from accounts.decorators import staff_check

# Create your views here.

#------------------------------------------------------------------------
@staff_check
def dashboard_view(request, *args, **kwargs):
    '''Dashboard for all user info'''

    cust = Account.objects.all().count()
    count_orders = ornamentOrder.objects.all().count()

    context = {
        'page_title': "Dashboard",
        'count_cust': cust,
        'count_orders': count_orders,
    }
    return render(request, "dashboard/dashboard.html", context)


#------------------------------------------------------------------------
# @staff_check
def order_dashboard_view(request, *args, **kwargs):
    '''All info about user order'''

    cust = Account.objects.all()
    orders = ornamentOrder.objects.all().order_by('id')
    paginator = Paginator(orders, 50, orphans=20)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    context = {
        'page_title': "Orders",
        'customer': cust,
        'orders': page_obj,
    }
    return render(request, "dashboard/order_dashboard.html", context)


#------------------------------------------------------------------------
@staff_check
def customer_dashboard_view(request, *args, **kwargs):
    '''All Customers'''

    cust = Account.objects.all().order_by('id')
    paginator = Paginator(cust, 50, orphans=20)
    page_no = request.GET.get('page')
    page_obj = paginator.get_page(page_no)

    context = {
        'page_title': "Customers",
        'customer': page_obj,
    }
    return render(request, "dashboard/customer_dashboard.html", context)


#------------------------------------------------------------------------
# @staff_check
def customer_detail_dashboard_view(request, id):
    '''All orders based on customer we click'''
    
    cust_ac = Account.objects.filter(id=id).first()
    cust_acx = AccountExtention.objects.filter(account_id=id).first()
    cust_address = UserAddress.objects.filter(account_id=id).first()
    cust_orders = ornamentOrder.objects.filter(account_id=id).all()

    context = {
        'page_title': "Customers Details",
        'customer': cust_ac,
        'customerx': cust_acx,
        'customer_address': cust_address,
        'customer_orders': cust_orders,
    }
    return render(request, "dashboard/customer_detail_dashboard.html", context)


#------------------------------------------------------------------------
# @staff_check
# def customers_json(request, *args, **kwargs):
#     '''JSON data for all customers'''

#     print(kwargs)
#     upper = kwargs.get('num_cust')
#     lower = upper - 1
#     customers = list(Account.objects.values()[lower:upper])
#     return JsonResponse({'data': customers}, safe=False)