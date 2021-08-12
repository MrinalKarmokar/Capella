from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello, name='hello'),
    path('', views.youraccount_view, name='your_account'),
    path('your-addresses', views.youraddress_view, name='your_addresses'),
    path('your-profile', views.yourprofile_view, name='your_profile'),
    path('add-address', views.addaddresses_view, name='add_address'),

    path('change-address', views.changeaddresses_view, name='change_address'),
    path('change-name', views.changename_view, name='change_name'),
    path('change-email', views.changeemail_view, name='change_email'),
    path('change-phoneno', views.changephone_view, name='change_phone'),
    path('change-password', views.changepassword_view, name='change_password'),
    
    path('verify-email/<token_args>', views.verify_email_backend, name='verify_email'),
    path('verify-phone/<token_args>', views.verify_phone_backend, name='verify_phone'),
    path('reset-password', views.resetpassword_view, name='resetpassword'),
    path('reset-password/<uid_args>/<token_args>', views.resetpasswordconfirm_view, name='resetpasswordconfirm'),
]