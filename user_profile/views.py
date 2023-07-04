from django.shortcuts import render ,redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from user_profile.models import UserProfileModel

# ---------------------------------------------------------------
class SignUpView(FormView):
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        form = UserCreationForm()
        return render(request,'user_profile/signup.html',context={'form':form})
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            self._form_handling(form)
            return redirect('/')
        
    # ------------------------------
    def _form_handling(self,form):
        user=  form.save()
        UserProfileModel.objects.create(user= user)
        