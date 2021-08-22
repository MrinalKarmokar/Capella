import datetime

from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

today = datetime.datetime.now().date()
current_time = datetime.datetime.now().strftime("%H:%M:%S")

#--------------------------------------------------------------------------
def icon_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/icon.html', context)


#--------------------------------------------------------------------------
def index_view(request, *args, **kwargs):
    context = {
        "today" : today,
        "time" : current_time,
    }
    return render(request, 'pages/index.html', context)


#--------------------------------------------------------------------------
def email_verified_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/email_verification_done.html', context)


#--------------------------------------------------------------------------
def home_view(request, *args, **kwargs):

    first_name = request.session.get('first_name', default="Guest")

    context = {
        "today" : today,
        "time" : current_time,
        'first_name' : first_name,
    }

    return render(request, 'pages/home.html', context)


#--------------------------------------------------------------------------
def contact_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/contact.html', context)


#--------------------------------------------------------------------------
def necklaces_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/necklaces.html', context)


#--------------------------------------------------------------------------
def rings_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/rings.html', context)


#--------------------------------------------------------------------------
def necklaces_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/necklaces.html', context)


#--------------------------------------------------------------------------
def bracelets_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/bracelets.html', context)


#--------------------------------------------------------------------------
def earrings_view(request, *args, **kwargs):
    context = {}
    return render(request, 'pages/earrings.html', context)

#--------------------------------------------------------------------------
def about_view(request, *args, **kwargs):
    context={}
    return render(request, 'pages/about.html', context)
