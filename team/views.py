from django.shortcuts import render,get_object_or_404 ,redirect
from django.views import View
from team.forms import TeamEditForm
from team.models import Team
from django.contrib import messages

# ---------------------------------------------------------------
class EditTeam(View):
    
    template_name = "team/edit_team.html"
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        pk = kwargs['pk']
        context = self.get_context_data(pk=pk)
        return render(request,self.template_name,context)
        
    # ------------------------------
    def get_queryset(self,pk):
        return get_object_or_404(Team,created_by = self.request.user,pk=pk)
    
    # ------------------------------
    def get_context_data(self,**kwargs):
        context = dict()
        context['team'] = self.get_queryset(kwargs['pk'])
        context['form'] = TeamEditForm(instance=context['team'])
        return context
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        team = self.get_queryset(kwargs['pk'])
        form = TeamEditForm(request.POST,instance=team)
        if form.is_valid():
            form.save()
            messages.success(request,"Team Is Updated Successfully")
            return redirect('my-account')
        
        
