import uuid
from datetime import datetime

from capella.settings import TEMPLATES
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.cache import cache_control

from accounts.decorators import is_login, is_not_login
from accounts.forms import AccountForm
from accounts.models import Account, AccountExtention, UserAddress

# Create your views here.

now = datetime.now()
today = datetime.now().date()
current_time = datetime.now().strftime("%H:%M:%S")

#----------------------------------------------------------------------------

def hello(request, *args, **kwargs):
    context = {
        "today" : today,
        "time" : current_time,
    }
    return render(request, 'hello.html', context)


#--------------------------------------------------------------------------
@is_login
def youraccount_view(request, *args, **kwargs):
    '''(User Account Page) Page with options for changing/setting things'''

    context = {}
    return render(request, 'accounts/your_accounts.html', context)


#--------------------------------------------------------------------------
@is_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addaddresses_view(request, *args, **kwargs):
    '''Add Address Page'''

    return_url = ""
    if request.GET.get('return_url'):
        return_url = request.GET.get('return_url')
        
    if request.method == 'POST':
        address_flat = str(request.POST['address_flat'])
        address_area = str(request.POST['address_area'])
        address_landmark = str(request.POST['address_landmark'])
        address_city = str(request.POST['address_city'])
        address_state = str(request.POST['address_state'])
        address_zip = str(request.POST['address_zip'])
        address_type = str(request.POST['address_type'])
        id = request.session.get('id', default="")

        form_address = UserAddress(request.POST)

        context = {
            'form': form_address
        }
        try:
            instance = UserAddress(account_id=id, address_zip=address_zip, address_flat=address_flat, address_area=address_area, address_landmark=address_landmark, address_city=address_city, address_state=address_state, address_type=address_type)
            instance.save()
            return redirect('your_addresses')
        
        except Exception as e:
            print(e)
            return redirect('add_address')

    else:
        form = UserAddress()
        context = {
            'form': form,
            'return_url': return_url,
        }
    return render(request, 'accounts/add_address.html', context)


#--------------------------------------------------------------------------
@is_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changeaddresses_view(request, *args, **kwargs):
    '''Change User address Page'''

    id = request.session.get('id', default="")
    cust_ac = UserAddress.objects.filter(account_id=id).first()
    try:
        if cust_ac:
            flat = str(cust_ac.address_flat)
            area = str(cust_ac.address_area)
            landmark = str(cust_ac.address_landmark)
            city = str(cust_ac.address_city)
            state = str(cust_ac.address_state)
            zip = str(cust_ac.address_zip)
            type = str(cust_ac.address_type)

        if request.method == 'POST':

            if request.POST['address_flatUpdate']:
                address_flat = request.POST['address_flatUpdate']
                cust_ac.address_flat = address_flat
                cust_ac.save()
                flat = str(cust_ac.address_flat)

            if request.POST['address_areaUpdate']:
                address_area = request.POST['address_areaUpdate']
                cust_ac.address_area = address_area
                cust_ac.save()
                area = str(cust_ac.address_area)
            
            if request.POST['address_landmarkUpdate']:
                address_landmark = request.POST['address_landmarkUpdate']
                cust_ac.address_landmark = address_landmark
                cust_ac.save()
                landmark = str(cust_ac.address_landmark)

            if request.POST['address_cityUpdate']:
                address_city = request.POST['address_cityUpdate']
                cust_ac.address_city = address_city
                cust_ac.save()
                city = str(cust_ac.address_city)

            if request.POST['address_stateUpdate']:
                address_state = request.POST['address_stateUpdate']
                cust_ac.address_state = address_state
                cust_ac.save()
                state = str(cust_ac.address_state)

            if request.POST['address_zipUpdate']:
                address_zip = request.POST['address_zipUpdate']
                cust_ac.address_zip = address_zip
                cust_ac.save()
                zip = str(cust_ac.address_zip)

            if request.POST['address_typeUpdate']:
                address_type = request.POST['address_typeUpdate']
                cust_ac.address_type = address_type
                cust_ac.save()
                type = str(cust_ac.address_type)

            return redirect('your_addresses')
        
        else:
            context = {
                "flat": flat,
                "area": area,
                "landmark": landmark,
                "city": city,
                "state": state,
                "zip": zip,
                "type": type,
            }

            return render(request, 'accounts/change_address.html', context)

    except Exception as e:
        print("Exception: ", e)
        return redirect('your_addresses')


#--------------------------------------------------------------------------
@is_login
def youraddress_view(request, *args, **kwargs):
    '''Show User address Page'''

    id = request.session.get('id', default="")
    first_name = request.session.get('first_name', default="Guest")
    last_name = request.session.get('last_name', default="")
    email = request.session.get('email', default="")
    phone = request.session.get('phone', default="")

    context = {
        'id': id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
    }

    cust_ac = UserAddress.objects.filter(account_id=id).first()

    try:
        if cust_ac:
            print("Your Address: ", cust_ac)
            flat = str(cust_ac.address_flat)
            area = str(cust_ac.address_area)
            landmark = str(cust_ac.address_landmark)
            city = str(cust_ac.address_city)
            state = str(cust_ac.address_state)
            zip = str(cust_ac.address_zip)
            type = str(cust_ac.address_type)

            context = {
                'id': id,
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
            }

            return render(request, 'accounts/your_addresses.html', context)

        else:
            print("Address field is empty")
            return redirect('add_address')

    except Exception as e:
        print("Exception: ", e)
        return redirect('add_address')


#--------------------------------------------------------------------------
@is_login
def yourprofile_view(request, *args, **kwargs):
    '''User Profile Page (Name, Phone, Email, etc)'''
    id = request.session.get('id', default="")
    first_name = request.session.get('first_name', default="Guest")
    last_name = request.session.get('last_name', default="")
    email = request.session.get('email', default="")
    phone = request.session.get('phone', default="")
    token_phone = str(uuid.uuid4())
    cust_acx = AccountExtention.objects.filter(account_id=id).first()
    phone_is_verified = cust_acx.phone_is_verified

    context = {
        'id': id,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'phone_is_verified': phone_is_verified,
    }

    if request.method == 'POST':
        cust_acx.token_phone = token_phone
        cust_acx.save()
        phone_verify_link(request, phone, token_phone)

        return redirect('your_profile')
        
    else:
        return render(request, 'accounts/your_profile.html', context)


#--------------------------------------------------------------------------
@is_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changename_view(request, *args, **kwargs):
    '''Change User Name Page'''

    id = request.session.get('id', default="")
    first_name = request.session.get('first_name', default="Guest")
    last_name = request.session.get('last_name', default="")

    context = {
        'id': id,
        'first_name': first_name,
        'last_name': last_name,
    }

    if request.method == 'POST':
        cust_ac = Account.objects.filter(id=id).first()

        if request.POST['firstnameUpdate']:
            first_name_cg = request.POST['firstnameUpdate']
            cust_ac.first_name = first_name_cg
            cust_ac.save()
            request.session['first_name'] = str(cust_ac.first_name)

        if request.POST['lastnameUpdate']:
            last_name_cg = request.POST['lastnameUpdate']
            cust_ac.last_name = last_name_cg
            cust_ac.save()
            messages.success(request, "Name changed successfully")
            request.session['last_name'] = str(cust_ac.last_name)

        return redirect('your_profile')
        
    else:
        return render(request, 'accounts/change_name.html', context)


#--------------------------------------------------------------------------
@is_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changeemail_view(request, *args, **kwargs):
    '''Change User Email Page'''

    id = request.session.get('id', default="")
    first_name = request.session.get('first_name')
    email_old = request.session.get('email', default="")
    token_email = str(uuid.uuid4())

    context = {
        'id': id,
        'email_old': email_old,
    }

    if request.method == 'POST':
        email_new = request.POST['emailUpdate']
        password_req = request.POST['password']

        if (email_new or password_req) == "":
            messages.warning(request, "Please fill in all fields")
            return redirect('change_email')

        cust_ac = Account.objects.filter(id=id).first()
        cust_acx = AccountExtention.objects.filter(account_id=id).first()
        cust_acx.token_email = token_email
        cust_acx.save()

        try:
            if cust_ac:
                print("For Email change: ", cust_ac)

                if check_password(password_req, cust_ac.password):
                    print("Previous Email: ", cust_ac.email, cust_ac.password)
                    cust_ac.email = email_new
                    cust_acx.email_is_verified = False
                    cust_ac.save()
                    cust_acx.save()
                    email_verification(request, email_new, token_email, first_name)
                    messages.success(request, "Email changed successfully")
                    return redirect('login')

                else:
                    messages.warning(request, "Password is incorrect")
                    return redirect('change_email')

            else:
                messages.warning(request, "Something went wrong!")
                return redirect('change_email')
        
        except Exception as e:
            print(e)

    else:
        return render(request, 'accounts/change_email.html', context)


#--------------------------------------------------------------------------
@is_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changephone_view(request, *args, **kwargs):
    '''Change User Phone-No. Page'''

    id = request.session.get('id', default="")
    phone_old = request.session.get('phone', default="")
    token_phone = str(uuid.uuid4())

    context = {
        'id': id,
        'phone_old': phone_old,
    }

    if request.method == 'POST':
        phone_new = request.POST['phoneUpdate']
        password_req = request.POST['password']

        country_code = '+91'
        if phone_new[0] == "0":
            phone_new = phone_new[1:]
            
        phone_new = country_code + phone_new

        if (phone_new or password_req) == "":
            messages.warning(request, "Please fill in all fields")
            return redirect('change_phone')

        cust_ac = Account.objects.filter(id=id).first()
        cust_acx = AccountExtention.objects.filter(account_id=id).first()
        cust_acx.token_phone = token_phone
        cust_acx.save()

        try:
            if cust_ac:
                print("For Phone no. change: ", cust_ac)

                if check_password(password_req, cust_ac.password):
                    print("Previous Phone no.: ", cust_ac.phone, cust_ac.password)
                    cust_ac.phone = phone_new
                    cust_acx.phone_is_verified = False
                    cust_ac.save()
                    cust_acx.save()
                    # phone_verify_link(request, phone_new, token_phone)
                    request.session['phone'] = str(cust_ac.phone)
                    messages.success(request, "Phone no. changed successfully")
                    return redirect('your_profile')

                else:
                    messages.warning(request, "Password is incorrect")
                    return redirect('change_phone')

            else:
                messages.warning(request, "Something went wrong!")
                return redirect('change_phone')
        
        except Exception as e:
            print(e)
            messages.error(request, "Phone no.already exists")
            return redirect('change_phone')

    else:
        return render(request, 'accounts/change_phone.html', context)


#--------------------------------------------------------------------------
@is_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def changepassword_view(request, *args, **kwargs):
    '''Change Account Password Page'''

    context = {}
    if request.method == 'POST':
        password_old = request.POST['password_old']
        password_new1 = request.POST['password_new1']
        password_new2 = request.POST['password_new2']
        email = request.session.get('email', default="")

        if (password_old or password_new1 or password_new2) == "":
            messages.warning(request, "Please fill in all fields")
            return redirect('change_password')

        cust_ac = Account.objects.filter(email=email).first()

        try:
            if cust_ac:
                if check_password(password_old, cust_ac.password):
                    if password_new1 == password_new2:
                        if password_old == password_new1:
                            messages.warning(request, "Old password cannot be your New Password")
                            return redirect('change_password')
                        
                        new_password = make_password(password_new1)
                        cust_ac.password = new_password
                        cust_ac.save()
                        messages.success(request, "Password changed successfully")
                        return redirect('your_profile')

                    else:
                        messages.warning(request, "New Passwords does'nt match!")
                        return redirect('change_password')

                else:
                    messages.warning(request, "Current Password is incorrect")
                    return redirect('change_password')

            else:
                messages.warning(request, "Something went wrong!")
                return redirect('change_password')

        except Exception as e:
            print("Exception: ", e)

    else:
        return render(request, 'accounts/change_password.html', context)


#--------------------------------------------------------------------------
def hasNumbers(inputString):
    '''Checks if Login Page input is Phone or Email'''

    return any(char.isdigit() for char in inputString[0])
    

#--------------------------------------------------------------------------
@is_not_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_user_view(request, *args, **kwargs):
    '''User Login and set sessions'''

    context = {
        "today": today,
        "time": current_time,
    }
    return_url = None
    
    if request.method == 'POST':
        username_req = request.POST['username']
        password_req = request.POST['password']

        country_code = '+91'
        if hasNumbers(username_req):
            if username_req[0] == "0":
                username_req = username_req[1:]
        
            username_req = country_code + str(username_req)

        if (username_req or password_req) == "":
            messages.warning(request, "Please fill in all fields")
            return redirect('login')

        cust_ac = Account.objects.filter(Q(phone=username_req) | Q(email=username_req)).first()
        
        try:
            if cust_ac:
                print(cust_ac)
                id = cust_ac.id
                cust_acx = AccountExtention.objects.filter(account_id=id).first()

                if cust_acx.email_is_verified:
                    if check_password(password_req, cust_ac.password):
                        print(cust_ac.email, cust_ac.password)
                        print("You Logged In, Enjoy!")
                        messages.success(request, "You Logged In, Enjoy!")
                        request.session['id'] = str(cust_ac.id)
                        request.session['first_name'] = str(cust_ac.first_name)
                        request.session['last_name'] = str(cust_ac.last_name)
                        request.session['email'] = str(cust_ac.email)
                        request.session['phone'] = str(cust_ac.phone)

                        if request.GET.get('return_url'):
                            return_url = request.GET.get('return_url')
                            return HttpResponseRedirect(return_url)
                        else:
                            return_url = None
                            return redirect('home')

                    else:
                        messages.warning(request, "Password is incorrect")
                        return redirect('login')

                else:
                    messages.warning(request, "Please Verify your Account")
                    return redirect('login')
            
            else:
                messages.warning(request, "Email/Phone does'nt exists")
                return redirect('login')

        except Exception as e:
            print(e)
    
    else:
        return render(request, 'accounts/login.html', context)


#--------------------------------------------------------------------------
def logout_view(request):
    '''Logging Out Users and clearing sessions'''

    logout(request)
    return redirect('/')


#--------------------------------------------------------------------------
@is_not_login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def create_user_account_view(request, *args, **kwargs):
    '''User Sign Up Page'''
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        token_email = str(uuid.uuid4())

        country_code = '+91'
        if phone[0] == "0":
            phone = phone[1:]
            
        phone = country_code + phone

        form = AccountForm(request.POST)
        context = {
            "today" : today,
            "time" : current_time,
            'form': form
        }
        try:
            if form.is_valid():
                if password1 == password2:
                    try:
                        password1 = make_password(password1)
                        instance_ac = Account(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password1)
                        instance_ac.save()
                        cust_ac = Account.objects.filter(email=email).first()
                        id = cust_ac.id
                        instance_acx = AccountExtention(account_id=id, token_email=token_email)
                        instance_acx.save()
                        email_verification(request, email, token_email, first_name)
                        return redirect('login')

                    except Exception as e:
                        print(e)
                        messages.warning(request, "Account with this Phone No. already exists")
                        return redirect('signup')

                else:
                    messages.warning(request, "Password does'nt match!")
                    return redirect('signup')
            
            else:
                print(form.errors)
                messages.warning(request, form.errors)
                return redirect('signup')
        
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
            return redirect('signup')

    else:
        form = AccountForm()
        context = {
            "today": today,
            "time": current_time,
            'form': form
        }

    return render(request, 'accounts/signup.html', context)


#--------------------------------------------------------------------------
def email_verification(request, email_arg, token_arg, first_name):
    '''Send mail for Verification'''

    context = {
        'first_name': first_name,
        'token': token_arg,
    }

    html_content = render_to_string('accounts/email_verification_template.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        'CAPELLA | Your Email need to be verified!',
        text_content,
        settings.EMAIL_HOST_USER,
        [email_arg],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

    messages.info(request, "Please check your email to verify your account")

    return True


#--------------------------------------------------------------------------
def phone_verify_link(request, phone_arg, token_arg):
    '''Generate link for Phone-No. Verification'''

    email = request.session.get('email', default="")
    message = f'Send to: {phone_arg}, Copy this link to your browser to verify your phone no. http://127.0.0.1:8000/accounts/verify-phone/{token_arg}'
    cust_ac = Account.objects.filter(email=email).first()
    id = cust_ac.id
    cust_acx = AccountExtention.objects.filter(account_id=id).first()
    cust_acx.phone_verification_link = message
    cust_acx.save()
    # try:
    #     pywhatkit.sendwhatmsg(phone_arg, f'Copy this link to your browser to verify your phone no. http://127.0.0.1:8000/accounts/verify-phone/{token_arg}', now.strftime("%H"), now.strftime("%M"))
    
    # except:
    #     pywhatkit.sendwhatmsg(phone_arg, f'Copy this link to your browser to verify your phone no. http://127.0.0.1:8000/accounts/verify-phone/{token_arg}', now.strftime("%H"), now.strftime("%M"))

    messages.info(request, "Please check your Whatsapp to verify your Phone No. (message may arrive within 1hr)")

    return True


#--------------------------------------------------------------------------
def verify_email_backend(request, token_args):
    '''Email Verifying backend process for Signup'''

    try:
        obj = AccountExtention.objects.filter(token_email=token_args).first()
        if obj:
            obj.email_is_verified = True
            obj.save()
            print("Email Verified Successfully, Enjoy!")
            messages.info(request, "Email Verified Successfully, Enjoy!")
            return redirect('login')

        else:
            print("Account not verified")
            return HttpResponse("<h1>Email not Verified</h1>")

    except Exception as e:
        print(e)
        return HttpResponse("<h1>Something went wrong :(</h1>")


#--------------------------------------------------------------------------
def verify_phone_backend(request, token_args):
    '''Phone Verifying backend process'''

    try:
        obj = AccountExtention.objects.filter(token_phone=token_args).first()
        if obj:
            obj.phone_is_verified = True
            obj.save()
            print("Phone No. Verified Successfully, Enjoy!")
            context = {
                'status': "Phone No. Verified Successfully, Enjoy!",
            }
            return render(request, 'pages/status.html', context)
            
        else:
            print("Phone No. not verified")
            context = {
                'status': "Something went wrong, Phone no. not verified",
            }
            return render(request, 'pages/status.html', context)

    except Exception as e:
        print(e)
        return HttpResponse("<h1>Something went wrong :(</h1>")


#--------------------------------------------------------------------------
def resetpassword_view(request, *args, **kwargs):
    '''Reset Password'''
    context = {}
    if request.method == 'POST':
        email = request.POST['email']

        cust_ac = Account.objects.filter(email=email).first()

        try:
            if cust_ac:
                id = cust_ac.id
                cust_acx = AccountExtention.objects.filter(account_id=id).first()
                token_email = cust_acx.token_email
                uid = str(uuid.uuid4())
                cust_acx.changepass_uid = uid
                cust_acx.save()

                print("User found: ",cust_ac)
                send_mail_changepassword(request, email, token_email, uid)
                messages.info(request, "Please check your email to change your password")
                return render(request, 'accounts/reset_password.html', context)

            else:
                messages.warning(request, "No such email id")
                return render(request, 'accounts/reset_password.html', context)

        except Exception as e:
            print(e)
            return render(request, 'accounts/reset_password.html', context)
    
    else:
        return render(request, 'accounts/reset_password.html', context)


#--------------------------------------------------------------------------
def resetpasswordconfirm_view(request, uid_args, token_args):
    '''User Reset Password (Enter New Password)'''

    try:
        if request.method == 'POST':
            password1 = request.POST['password']
            password2 = request.POST['password2']

            if (password1 or password2) != "":
                objx = AccountExtention.objects.filter(Q(changepass_uid=uid_args) & Q(token_email=token_args)).first()
                id = objx.account_id
                obj = Account.objects.filter(id=id).first()
            else:
                messages.warning(request, "Fill in all fileds!")
                return render(request, 'accounts/new_password.html')

            if obj:
                if password1 == password2:
                    password1 = make_password(password1)
                    obj.password = password1
                    obj.save()

                    messages.info(request, "Password changed successfully, Please login using new password")
                    return redirect('login')

                else:
                    messages.warning(request, "Password does'nt match!")
                    return render(request, 'accounts/new_password.html')

            else:
                messages.warning(request, "Invalid link")
                return render(request, 'accounts/reset_password.html')

        else:
            return render(request, 'accounts/new_password.html')

    except Exception as e:
        print(e)
        return HttpResponse("<h1>Something went wrong :(</h1>")

    
#--------------------------------------------------------------------------
def send_mail_changepassword(request, email_arg, token_arg, uid_arg):
    '''Verifying Process for Reset Password'''

    context = {
        'token': token_arg,
        'uid': uid_arg,
    }

    html_content = render_to_string('accounts/change_email_verification_template.html', context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        'CAPELLA | Request for password change',
        text_content,
        settings.EMAIL_HOST_USER,
        [email_arg],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

    messages.info(request, "Please check your email to verify your account")

    return True
