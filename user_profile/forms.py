from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    
    username = forms.CharField(label='',widget=forms.TextInput(attrs={
        'placeholder':"Your Username",
        "class":"w-full px-6 py-4 bg-gray-200 rounded-xl"
    }))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        'placeholder':"Your Password",
        "class":"w-full px-6 py-4 bg-gray-200 border-2 rounded-xl"
    }))
    
    
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
    
    username = forms.CharField(label='',widget=forms.TextInput(attrs={
        'placeholder':"Your Username",
        "class":"w-full px-6 py-4 bg-gray-200 rounded-xl"
    }))
    password1 = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        'placeholder':"Your Password",
        "class":"w-full px-6 py-4 bg-gray-200 border-2 rounded-xl"
    }))
    password2 = forms.CharField(label='',widget=forms.PasswordInput(attrs={
        'placeholder':"Confirm Your Password",
        "class":"w-full px-6 py-4 bg-gray-200 border-2 rounded-xl"
    }))
    
    
    