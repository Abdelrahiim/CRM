from django.shortcuts import render ,redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

from .models import UserProfileModel
class SignInView(FormView):
    
    
    def get(self,request,*args, **kwargs):
        form = UserCreationForm()
        return render(request,'user_profile/signup.html',context={'form':form})
    
    
    def post(self,request,*args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=  form.save()
            UserProfileModel.objects.create(user= user)
            return redirect('/')
        