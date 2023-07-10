from typing import Optional, Type
from django.forms import ValidationError
from django.forms.forms import BaseForm
from django.shortcuts import render ,redirect
from django.views import View
from django.views.generic import FormView
from user_profile.forms import CustomUserCreationForm
from team.models import Team
from user_profile.models import UserProfileModel
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.auth import authenticate, login
# ---------------------------------------------------------------
class SignUpView(FormView):
    template_name = 'user_profile/signup.html'
    form_class = CustomUserCreationForm
    # ------------------------------
    def get(self,request,*args, **kwargs):
        form = self.form_class()
        return render(request,self.template_name,context={'form':form})
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = self._form_handling(form)
            login(request,user=user)
            return redirect('dashboard:')
        raise ValidationError("Error Validate The Form")
    
    # ------------------------------
    def _form_handling(self,form):
        team = self._get_team()
        user=  form.save()
        team.members.add(user)
        UserProfileModel.objects.create(user= user,active_team=team)
        return user
        
    
    def _get_team(self):
        return Team.objects.filter(name="Operations").first()
        
        
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
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id))[0]

    