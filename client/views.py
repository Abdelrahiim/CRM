from typing import Any, Dict
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from client.models import Client
from client.forms import AddClientForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from team.models import Team
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
# Create your views here.


# -------------------------------------------------------------
class ClientList(LoginRequiredMixin, View):
    template_name = "clients\clients.html"
    context_object_name = 'clients'
    
    # ------------------------------
    def get(self, request):
        context = self.get_context_data(request)
        return render(request,self.template_name, context)
    
    # ------------------------------
    def get_context_data(self, request):
        context = {}
        clients = Client.objects.filter(created_by = request.user)
        context[self.context_object_name] = self.get_pagination(request,queryset=clients)
        return context
    
    # ------------------------------
    def get_pagination(self,request,queryset):
        paginator = Paginator(queryset, 5)  
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.get_page(page_number)  
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        return page_obj
    
    


# -------------------------------------------------------------
class SingleClient(LoginRequiredMixin, View):
    template_name = "clients/single_client.html"
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        context = self.get_context_data(user = request.user,pk=pk)
        return render(request, self.template_name, context)
    
    # ---------------------------------------
    def get_context_data(self, **kwargs):
        context = {}
        context["client"] = get_object_or_404(Client, created_by=kwargs['user'], pk=kwargs['pk'])
        return context
    


# -------------------------------------------------------------
class CreateNewClient(LoginRequiredMixin, View):
    template_name = "clients/create-client.html"
    
    # ------------------------------
    def get(self, request):
        context = self.get_context_data(user=request.user)
        return render(request, self.template_name, context=context)

    # ------------------------------
    def post(self, request):
        form = self.get_form(data= request.POST)
        
        if form.is_valid():
            self._create_client(request.user, form)
            messages.success(request, "Client Created Successfully")
            return redirect("client:list")
        raise ValidationError("Error Validate The Form")

    # ------------------------------
    def _create_client(self,user, form: AddClientForm):
        client = form.save(commit=False)
        client.created_by = user
        client.team = self._get_team(user)
        client.save()
        
        
    # ------------------------------
    def _get_team(self,user):
        return Team.objects.filter(created_by= user).first()
    
    # -------------------------------------------
    def get_form(self,**kwargs) -> AddClientForm:
        if kwargs:
            data= kwargs['data']
            form = AddClientForm(data)
        else:
            form = AddClientForm()
        return form
            
    def get_context_data(self,user):
        context = dict()
        context["form"] = self.get_form()
        context['team'] = self._get_team(user)
        context['title'] = 'Edit'
        return context
    
        
        

# ---------------------------------------------------------------
class UpdateClient(LoginRequiredMixin, View):
    template_name = "clients/create-client.html"
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(pk = kwargs['pk'])
        return render(request,self.template_name , context)
    
    # ------------------------------
    def get_context_data(self, **kwargs):
        context = {}
        lead = self.get_queryset(pk = kwargs['pk'])
        context["form"] = self.get_form(instance = lead)
        context['title'] = 'Edit'
        return context
    
    # ------------------------------
    def get_queryset(self,**kwargs):
        return get_object_or_404(Client, created_by=self.request.user, pk=kwargs['pk'])

    # ------------------------------
    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        client = get_object_or_404(Client, created_by=request.user, pk=pk)
        
        form = self.get_form(data=request.POST,instance = client)
        
        if form.is_valid():
            form.save()
            messages.success(request, "The Client Was edited Successfully")
            return redirect("client:list")
    
    # ------------------------------    
    def get_form(self,**kwargs) -> AddClientForm:
        if kwargs.get('data'):
            form = AddClientForm(kwargs.get('data'),instance=kwargs['instance'])
        else:
            form = AddClientForm(instance=kwargs.get('instance'))
        return form




class DeleteClient(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        self._delete_client(request.user, pk)
        messages.success(request, "Client Deleted Successfully")
        return redirect("client:list")

    # ------------------------------
    def _delete_client(self, user, pk):
        client = get_object_or_404(Client, created_by=user, pk=pk)
        client.delete()
