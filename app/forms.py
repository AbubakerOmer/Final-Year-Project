from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.db import models
from django import forms
from .models import *
from django import forms

class Contact(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = '__all__'

class HospitalForm(forms.ModelForm):
    class Meta:
        model=Hospital
        fields='__all__'
class BankForm(forms.ModelForm):
    class Meta:
        model=Bank
        fields='__all__'

class AsyForm(forms.ModelForm):
    class Meta:
        model=Assylum
        fields='__all__'
class RefForm(forms.ModelForm):
    class Meta:
        model=Refuse
        fields='__all__'

class GpForm(forms.ModelForm):
    class Meta:
        model=Gp
        fields='__all__'


class CustomerUserForm(forms.ModelForm):

    class Meta:
        model=User
        fields=['username','password','email']
        widgets = {
        'password': forms.PasswordInput()
        }
class CustomerForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['mobile','profile_pic']

CATEGEORY_CHOICES  = (
    ("Emergency_Support", "Emergency_Support"),
    ("Fix_Meeting", "Fix_Meeting"),
    ("Others", "Others"),
    ("Direct_Meeting", "Direct_Meeting"),
)

class QueryForm(forms.ModelForm):
    category_type = forms.ChoiceField(choices=CATEGEORY_CHOICES)

    class Meta:
        model=Query
        exclude = ["user","currenstatus","status","assign"]

STATUS_CHOICES = (

    ("PENDING", "PENDING"),
    ("APPROVED", "APPROVED"),
    ("REJECTED", "REJECTED"),)

class QueryStatus(forms.ModelForm):
    # category_type = forms.ChoiceField(choices=CATEGEORY_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
   
    class Meta:
        model = Query
        exclude = ["currenstatus","assign",'user']



class ConsellorForm(forms.ModelForm):
    class Meta():
        model= Query
        fields=['assign']


class EditProfileForm(UserChangeForm):
    template_name='/something/else'

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


