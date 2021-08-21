import razorpay
from django.shortcuts import render
from capella.settings import RAZORPAY_PUBLIC_KEY, RAZORPAY_PRIVATE_KEY
from django.views.decorators.csrf import csrf_exempt

from .models import Payment_info

# Create your views here.

def payment_home_view(request):

    if request.method == "GET" or "POST":
        amount_arg = request.GET['amount']
        context = {
            'firstname':request.session.get('firstname', default=""),
            'lastname':request.session.get('lastname', default=""),
            'email':request.session.get('email', default=""),
            'phone':request.session.get('phone', default=""),
            'amount': amount_arg,
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
                'amount':amount/100,
                'payment':payment,
                'RAZORPAY_PUBLIC_KEY': RAZORPAY_PUBLIC_KEY,
            }

            return render(request, "payment/payment_home.html", context)
        
        else:
            return render(request, "payment/payment_home.html", context)


@csrf_exempt
def payment_success_view(request, *args, **kwargs):
    context = {}
    return render(request, "payment/success.html", context)