from accounts.decorators import is_login
import razorpay
from capella.settings import RAZORPAY_PRIVATE_KEY, RAZORPAY_PUBLIC_KEY
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from order.models import ornamentOrder
from accounts.models import Account, UserAddress

# from .models import Payment_info

# Create your views here.

@is_login
def payment_home_view(request):
    try:
        id = request.session.get('id', default="")
        address = UserAddress.objects.filter(account_id=id).first()

        flat = address.address_flat
        area = address.address_area
        city = address.address_city
        state = address.address_state
        zip = address.address_zip

        if request.method == "GET" or "POST":
            amount_arg = request.GET['amount']
            order_id_arg = request.GET['order_id']
            context = {
                'firstname':request.session.get('firstname', default=""),
                'lastname':request.session.get('lastname', default=""),
                'email':request.session.get('email', default=""),
                'phone':request.session.get('phone', default=""),
                'amount': amount_arg,
                'order_id': order_id_arg,
            }

            if request.method == "POST":
                amount = int(amount_arg)*100
                client = razorpay.Client(auth=(RAZORPAY_PUBLIC_KEY, RAZORPAY_PRIVATE_KEY))
                payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})

                context = {
                    'firstname':request.session.get('firstname', default=""),
                    'lastname':request.session.get('lastname', default=""),
                    'email':request.session.get('email', default=""),
                    'phone':request.session.get('phone', default=""),
                    'order_id': order_id_arg,
                    'flat': flat,
                    'area': area,
                    'city': city,
                    'state': state,
                    'zip': zip,
                    'amount':int(amount/100),
                    'payment':payment,
                    'RAZORPAY_PUBLIC_KEY': RAZORPAY_PUBLIC_KEY,
                }

                return render(request, "payment/payment_home.html", context)
            
            else:
                return render(request, "payment/payment_home.html", context)
        
    except Exception as e:
        print(e)
        raise Http404("Page not found....")


@csrf_exempt
def payment_success_view(request, order_id):
    context = {}
    try:
        order = ornamentOrder.objects.filter(order_id=order_id).first()
        account = Account.objects.filter(id=order.account_id).first()
        if account.email==request.session.get('email', default="") and account.phone==request.session.get('phone', default=""):
            order.paid = True
            order.save()
            return render(request, "payment/success.html", context)
        else:
            raise Http404("Page not found....")
    
    except Exception as e:
        print(e)
        raise Http404("Page not found....")
