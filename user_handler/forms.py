from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import UserBase
from django.contrib.auth import get_user_model

class UserForm(UserCreationForm, ModelForm):
    username = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required =  True)
    last_name = forms.CharField(required =True)

    class Meta(UserCreationForm):
        model = UserBase
        fields = ['username','first_name','last_name','email']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(max_length = 32, widget= forms.PasswordInput)

    class Meta: 
        fields = ['username','password']