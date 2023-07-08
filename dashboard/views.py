from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Lead
from client.models import Client
from team.models import Team
# Create your views here.

class DashBoard(LoginRequiredMixin,View):
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        context = self.get_context_data(**kwargs)
        return render(request,'dashboard/dashboard.html',context=context)
    
    # ------------------------------
    def get_context_data(self, **kwargs):
        context = dict()
        team = self._get_team(self.request.user)
        context['leads'] = self._get_first_five_leads(team)
        context['clients'] = self._get_first_five_clients(team)
        return context
    
    # ------------------------------
    def _get_team(self,user):
        return Team.objects.filter(created_by=user).first()
    
    # ------------------------------
    def _get_first_five_leads(self,team):
        return  Lead.objects.filter(team= team,convert_to_client = False).order_by('-modified_at')[:5]

    # ------------------------------  
    def _get_first_five_clients(self,team):
        return Client.objects.filter(team = team).order_by('-modified_at')[:5]
        
        
