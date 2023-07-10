from django.shortcuts import render,get_object_or_404 ,redirect
from django.views import View ,generic
from team.forms import TeamEditForm
from team.models import Team
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q

class TeamList(LoginRequiredMixin,View):
    template_name =  'team/teams.html'
    
    def get(self,request,*args, **kwargs):
        context = self.get_context_data()
        return render(request,self.template_name,context)
    def get_queryset(self):
        return Team.objects.filter(created_by=self.request.user) or Team.objects.filter(members__id =self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context={}
        context["teams"] = self.get_queryset()
        print(context['teams'])
        return context
    
    

class TeamDetails(LoginRequiredMixin,View):
    template_name = "team/team_detail.html"
    
    def get(self,request,*args, **kwargs):
        context = self.get_context_data(user=request.user,pk=kwargs['pk'])
        
        return render(request,self.template_name,context)
    
    def get_queryset(self,user,pk):
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id)).first()
        
    def get_context_data(self, **kwargs):
        context = {}
        context["team"] = self.get_queryset(kwargs['user'],kwargs['pk']) 
        return context
    

# ---------------------------------------------------------------
class EditTeam(LoginRequiredMixin,View):
    
    template_name = "team/edit_team.html"
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        pk = kwargs['pk']
        context = self.get_context_data(user=request.user,pk=pk)
        return render(request,self.template_name,context)
        
    # ------------------------------
    def get_queryset(self,user,pk):
        return get_object_or_404(Team,created_by = user,pk=pk)
    
    # ------------------------------
    def get_context_data(self,**kwargs):
        context = dict()
        context['team'] = self.get_queryset(kwargs['user'],kwargs['pk'])
        context['form'] = TeamEditForm(instance=context['team'])
        return context
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        team = self.get_queryset(request.user,kwargs['pk'])
        form = TeamEditForm(request.POST,instance=team)
        if form.is_valid():
            form.save()
            messages.success(request,"Team Is Updated Successfully")
            return redirect('my-account')
        
        
