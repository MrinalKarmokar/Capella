import razorpay
from django.shortcuts import render

from .models import Payment_info

# Create your views here.

def payment_home_view(request, *args, **kwargs):
    
    context = {
        'firstname':request.session.get('firstname', default=""),
        'lastname':request.session.get('lastname', default=""),
        'email':request.session.get('email', default=""),
        'phone':request.session.get('phone', default=""),
    }

    if request.method == "POST":
        amount = int(request.POST.get("amount"))*100
        client = razorpay.Client(auth=("rzp_test_vBNvIpwC6hRjBo", "394FGxSoWzXcd8KEGGtqzvTM"))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
        print("Amount", amount)
        payment_info = Payment_info(name=request.session.get('firstname', default=""), amount=amount, payment_id=payment['id'])
        print("PAYMENT INFO: ", payment_info)

        context = {
            'firstname':request.session.get('firstname', default=""),
            'lastname':request.session.get('lastname', default=""),
            'email':request.session.get('email', default=""),
            'phone':request.session.get('phone', default=""),
            'amount':amount/100,
            'payment':payment,
        }

        return render(request, "payment/payment_home.html", context)
    
    else:
        return render(request, "payment/payment_home.html", context)
