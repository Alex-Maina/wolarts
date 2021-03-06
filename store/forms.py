from django.forms import ModelForm
from .models import Order, Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms 
from django.contrib import messages

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields ='__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'password1', 'password2']