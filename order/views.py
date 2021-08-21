import uuid
from datetime import date

from django.http.response import HttpResponse, HttpResponseRedirect
from accounts.models import Account, AccountExtention, UserAddress
from django.contrib import messages
from django.shortcuts import redirect, render

from order.models import ornamentOrder

from accounts.decorators import is_login
today = date.today()

# Create your views here.

#--------------------------------------------------------------------------
@is_login
def place_order_view(request, *args, **kwargs):
    '''Place Order Page'''

    id = request.session.get('id', default="")
    first_name = request.session.get('first_name', default="Guest")
    try:
        cust_address = UserAddress.objects.filter(account_id=id).first()
        print("Address:",cust_address)
        if cust_address == None:
            messages.warning(request, "Please save your address before placing order")
            return redirect(f'add_address')
    
    except Exception as e:
        print(e)
        messages.warning(request, "Something went wrong, try again")
        return redirect('place_order')
        
    context = {
        'first_name' : first_name 
    }
    try:            
        cust_acx = AccountExtention.objects.filter(account_id=id).first()
        if cust_acx.email_is_verified:
            if request.method == 'POST':
                order_id = f"C-{today.year}{today.month}{today.day}-{uuid.uuid1().time_low}"
                image = request.FILES['ref_image']
                metal_choice = request.POST.get('metal_choice', "")
                gold_quality = request.POST.get('gold_quality', "")
                budget = request.POST.get('budget', "")
                quantity = request.POST.get('quantity', "")
                design_insight = request.POST.get('design_insight', "")
                instructions = request.POST.get('instructions', "")

                order_ins = ornamentOrder(account_id=id, image_url=image, order_id=order_id, metal_choice=metal_choice, gold_quality=gold_quality, quantity=quantity, budget=budget, instructions=instructions, design_insight=design_insight)
                order_ins.save()
                
                messages.success(request, "Order Placed")
                return redirect('your_orders')

            else:
                return render(request, 'order/place_order.html', context)
        
        else:
            messages.warning(request, "Please verify your email before that action")
            return redirect('login')
        
    except Exception as e:
        print(e)
        messages.warning(request, "Something went wrong, try again")
        return redirect('place_order')


#--------------------------------------------------------------------------
@is_login
def your_order_view(request, *args, **kwargs):
    '''Shows Users Order'''

    context = {}
    id = request.session.get('id', default="")
    first_name = request.session.get('first_name', default="Guest")
    last_name = request.session.get('last_name', default="")
    email = request.session.get('email', default="")
    phone = request.session.get('phone', default="")
    
    try:
        cust_address = UserAddress.objects.filter(account_id=id).first()
        flat = str(cust_address.address_flat)
        area = str(cust_address.address_area)
        landmark = str(cust_address.address_landmark)
        city = str(cust_address.address_city)
        state = str(cust_address.address_state)
        zip = str(cust_address.address_zip)
        type = str(cust_address.address_type)
    
    except Exception as e:
        print(e)
        messages.warning(request, "Add your address!")
        return redirect('your_account')
    
    try:
        order_ins = ornamentOrder.objects.filter(account_id=id).all().order_by('-id')
        order_id_list = []
        for data in order_ins:
            if data.approved and not data.paid and not data.completed:
                order_id_list.append(data.order_id)
                messages.info(request, f"Order No. #{data.order_id} is Approved")

        context = {
            'ornament_orders': order_ins,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'flat': flat,
            'area': area,
            'landmark': landmark,
            'city': city,
            'state': state,
            'zip': zip,
            'type': type,
            'order_id_list': order_id_list,
        }

        return render(request, 'order/your_order.html', context)
        
    except Exception as e:
        print(e)
        messages.warning(request, "You have'nt placed any order")
        return redirect('your_account')