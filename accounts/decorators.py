from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect, render

from accounts.models import AccountExtention


def is_login(get_response):
    '''check that user is logged in'''

    def middleware(request):
        return_url = request.META['PATH_INFO']

        if request.session.get('email', default="") == "":
            messages.warning(request, "Please login before that action")
            return redirect(f'../login?return_url={return_url}')

        response = get_response(request)

        return response

    return middleware


def is_not_login(get_response):
    '''check that user is NOT logged in'''
    
    def middleware(request):
        if request.session.get('email', default="") != "":
            return redirect('home')

        response = get_response(request)

        return response

    return middleware


def staff_check(get_response):
    '''check that user is staff'''
    
    def middleware(request, *args, **kwargs):
        id = request.session.get('id')
        try:
            cust_acx = AccountExtention.objects.filter(account_id=id).first()
            print(cust_acx.permission)

            if cust_acx.permission=='superuser' or cust_acx.permission=='staff':
                response = get_response(request)
                return response
            
            else:
                print("1")
                raise Http404("Page not found :( ")
        
        except:
            print("2")
            raise Http404("Page not found :( ")

    return middleware


def superuser_check(get_response):
    '''check that user is superuser'''
    
    def middleware(request):
        id = request.session.get('id')
        try:
            cust_acx = AccountExtention.objects.filter(account_id=id).first()
            
            if cust_acx.permission=='superuser':
                response = get_response(request)
                return response

            else:
                raise Http404("Page not found :( ")
        
        except:
            raise Http404("Page not found :( ")

    return middleware
