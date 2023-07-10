import csv
from typing import Any, Dict
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from client.models import Client
from client.forms import ClientFileForm, ClientForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from team.models import Team
from django.db.models import Q
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
    form_class = CommentForm
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        context = self.get_context_data(user = request.user,pk=pk)
        return render(request, self.template_name, context)
    
    # ---------------------------------------
    def get_context_data(self, **kwargs):
        context = {}
        context["client"] = get_object_or_404(Client, created_by=kwargs['user'], pk=kwargs['pk'])
        context['form'] = self.get_form()
        context['file_form'] = ClientFileForm()
        return context
    
    # -------------------------------------------
    def get_form(self, **kwargs) :
        if kwargs:
            data = kwargs["data"]
            form = self.form_class(data)
        else:
            form = self.form_class()
        return form
    # -------------------------------------------
    def post(self, request, *args, **kwargs):
        """
        For Adding Comment
        """
        
        pk = kwargs['pk']
        form = self.get_form(data=request.POST)
        context = self.get_context_data(user=request.user,pk=pk)
        if form.is_valid(): 
            self._create_comment(client=context['client'],form=form)
            messages.success(request, "The Comment Was Created Successfully")
            return redirect("client:details",pk=pk)

        raise ValidationError("Error Validate The Form")
            
            
    # -------------------------------------------
    def _create_comment(self,client,form):
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.team = self._get_team(self.request.user)
        comment.client = client
        comment.save()
        
    # ------------------------------
    def _get_team(self, user):
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id))[0]

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
    def _create_client(self,user, form: ClientForm):
        client = form.save(commit=False)
        client.created_by = user
        client.team = self._get_team(user)
        client.save()
        
        
    # ------------------------------
    def _get_team(self,user):
        return Team.objects.filter(created_by= user)[0]
    
    # -------------------------------------------
    def get_form(self,**kwargs) -> ClientForm:
        if kwargs:
            data= kwargs['data']
            form = ClientForm(data)
        else:
            form = ClientForm()
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
        client = self.get_queryset(pk = kwargs['pk'])
        context["form"] = self.get_form(instance = client)
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
    def get_form(self,**kwargs) -> ClientForm:
        if kwargs.get('data'):
            form = ClientForm(kwargs.get('data'),instance=kwargs['instance'])
        else:
            form = ClientForm(instance=kwargs.get('instance'))
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



# ---------------------------------------------------------------
class UploadFileView(LoginRequiredMixin,View):
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        form = ClientFileForm(request.POST,request.FILES)
        
        if form.is_valid():
            self.form_handling(pk,form,request.user)
            messages.success(request,"File Uploaded Successfully")
            return redirect("client:details",pk=pk)

        raise ValidationError("Error Validate The Form")
    
    # -----------------------------------------------------------
    def form_handling(self,pk,form:ClientFileForm,user):
        file = form.save(commit=False)
        file.team = self._get_team(user)
        file.client_id = pk
        file.created_by = user
        file.save()
        
    # ------------------------------
    def _get_team(self, user):
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id))[0]


@login_required
def client_export(request):
    """
    export Clients Data As CSv files
    """
    clients = Client.objects.filter(created_by = request.user).all()
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="clients.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["CLient", "Email"  ,"Description", "Created at"])
    
    for client in clients:
        writer.writerow([client.name,client.email,client.description,client.created_at])

    return response