from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
   password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))
   phone = forms.CharField(label="Phone No.")

   class Meta:
      model = Account
      fields = [
         "first_name",
         "last_name",
         "email",
         "phone",
         "password",
      ]
      widgets = {
         'first_name':forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
         'last_name':forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
         'password':forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
         'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
         'phone': forms.TextInput(attrs={'placeholder': 'Enter Phone No.'})
      }