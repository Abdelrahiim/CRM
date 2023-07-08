from typing import Optional, Type
from django.forms import ValidationError
from django.forms.forms import BaseForm
from django.shortcuts import render ,redirect
from django.views import View
from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm
from team.models import Team
from user_profile.models import UserProfileModel
from django.contrib.auth.mixins import LoginRequiredMixin


# ---------------------------------------------------------------
class SignUpView(FormView):
    template_name = 'user_profile/signup.html'
    form_class = UserCreationForm
    # ------------------------------
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            self._form_handling(form)
            return redirect('/')
        raise ValidationError("Error Validate The Form")
    
    # ------------------------------
    def _form_handling(self,form):
        user=  form.save()
        UserProfileModel.objects.create(user= user)
        
        
# ---------------------------------------------------------------
class MyAccountView(LoginRequiredMixin,View):
    template_name = "user_profile/profile.html"
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        context= self.get_context_data(**kwargs)
        return render(request,self.template_name,context= context)
    
    # ------------------------------
    def get_context_data(self, **kwargs):
        context = dict()
        context["team"] = self._get_team(self.request.user)
        return context
    
    # ------------------------------
    def _get_team(self,user):
        return Team.objects.filter(created_by= user).first()
    