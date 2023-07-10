from typing import Any, Dict
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.core.paginator import Paginator ,EmptyPage , PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.forms import LeadForm ,CommentForm , LeadFileForm
from leads.models import Lead
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
from client.models import Client , ClientComment
from team.models import Team
from django.db.models import Q


# --------------------------------------------------------------
class ListAllLeads(LoginRequiredMixin, View):
    template_name = "leads/leads.html"

    # ------------------------------
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request)
        return render(request, self.template_name, context)

    # ------------------------------
    def get_context_data(self, request):
        context = {}
        leads = Lead.objects.filter(
            created_by=request.user, convert_to_client=False
        )
        
        context['leads'] = self.get_pagination(request,queryset=leads)
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
        


# --------------------------------------------------------------
class SingleLead(LoginRequiredMixin, View):
    template_name = "leads/single_lead.html"
    form_class = CommentForm

    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        context = self.get_context_data(user=request.user,pk=pk)
        return render(request, self.template_name,context)
    
    def get_context_data(self, **kwargs):
        context = {}
        context["lead"] = get_object_or_404(Lead, created_by=kwargs['user'], pk=kwargs['pk'])
        
        context['form'] = self.get_form()
        context['file_form'] = LeadFileForm()
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
            self._create_comment(lead=context['lead'],form=form)
            messages.success(request, "The Comment Was Created Successfully")
            return redirect("leads:details",pk=pk)

        raise ValidationError("Error Validate The Form")
            
            
    # -------------------------------------------
    def _create_comment(self,lead,form):
        comment = form.save(commit=False)
        comment.created_by = self.request.user
        comment.team = self._get_team(self.request.user)
        comment.lead = lead
        comment.save()
        
    # ------------------------------
    def _get_team(self, user):
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id))[0]


# --------------------------------------------------------------
class AddLeadView(LoginRequiredMixin, View):
    template_name = "leads/create_lead.html"

    # ------------------------------
    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(request.user)
        return render(request, self.template_name, context)

    # ------------------------------
    def post(self, request, *args, **kwargs):
        form = self.get_form(data=request.POST)

        if form.is_valid():
            self._create_lead(request.user, form)

            messages.success(request, "The Lead Was Created Successfully")
            return redirect("leads:list")

        raise ValidationError("Error Validate The Form")

    # ------------------------------
    def _create_lead(self, user, form: LeadForm):
        lead = form.save(commit=False)
        lead.created_by = user
        lead.team = self._get_team(user)
        lead.save()

    # ------------------------------
    def _get_team(self, user):
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id))[0]

    # -------------------------------------------
    def get_form(self, **kwargs) -> LeadForm:
        if kwargs:
            data = kwargs["data"]
            form = LeadForm(data)
        else:
            form = LeadForm()
        return form

    # -----------------------------------------------
    def get_context_data(self, user):
        context = dict()
        context["form"] = self.get_form()
        context["team"] = self._get_team(user)
        
        context["title"] = "Create"
        return context




# --------------------------------------------------------------
class UpdateLead(LoginRequiredMixin, View):
    template_name = "leads/create_lead.html"

    # ------------------------------
    def get(self, request, *args, **kwargs) -> HttpResponse:
        context = self.get_context_data(pk = kwargs['pk'])
        return render(request, self.template_name, context)

    # ------------------------------
    def get_context_data(self, **kwargs):
        context = {}
        lead = self.get_queryset(pk = kwargs['pk'])
        context["form"] = self.get_form(instance = lead)
        context["title"] = "Edit"
        return context

    # ------------------------------
    def get_queryset(self,**kwargs):
        return get_object_or_404(Lead, created_by=self.request.user, pk=kwargs['pk'])
    
    # ------------------------------
    def post(self, request, *args, **kwargs):
        
        lead = get_object_or_404(Lead, created_by=request.user,pk=kwargs.get('pk'))
        form = self.get_form(data=request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "The Lead Was edited Successfully")
            return redirect("leads:list")
        
        raise ValidationError("Error Validate The Form")

    # ------------------------------
    def get_form(self, **kwargs) :
        if kwargs.get('data') :
            form = LeadForm(kwargs['data'] , instance=kwargs["instance"])
        else:
            form = LeadForm(instance=kwargs["instance"])
        return form


# --------------------------------------------------------------
class DeleteLead(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        self._delete_lead(request, pk)
        return redirect("leads_list")

    # ------------------------------
    def _delete_lead(self, request, pk):
        lead = get_object_or_404(Lead, pk=pk, created_by=request.user)
        lead.delete()
        messages.success(request, "The Lead Was Deleted Successfully")


# ---------------------------------------------------------------
class ConvertToClient(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        lead = get_object_or_404(Lead, pk=pk, created_by=request.user)
        team = self._get_team(request.user)
        self._update_lead(request.user, lead, team)
        messages.success(request, "Lead Is Converted To Client Successfully")
        return redirect("leads:list")

    # ------------------------------
    def _update_lead(self, user, lead, team):
        
        # convert Lead Comm
        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=user,
            team=team,
        )
        
        lead.convert_to_client = True
        lead.save()
        
        comments = lead.comments_lead.all()
        for comment in comments:
            self.convert_comment(comment,client)
            
    # ------------------------------
    def convert_comment(self,comment,client):
        
        # Convert Lead Comment To Client Comment
        new_comment = ClientComment.objects.create(
            content = comment.content,
            created_by = comment.created_by,
            team = comment.team,
            client = client,
        )
        
    # ------------------------------
    def _get_team(self, user):
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id))[0]



# ---------------------------------------------------------------
class UploadFileView(LoginRequiredMixin,View):
    
    # ------------------------------
    def post(self,request,*args, **kwargs):
        pk = kwargs.get('pk')
        form = LeadFileForm(request.POST,request.FILES)
        
        if form.is_valid():
            self.form_handling(pk,form,request.user)
            messages.success(request,"File Uploaded Successfully")
            return redirect("leads:details",pk=pk)

        raise ValidationError("Error Validate The Form")
    
    # -----------------------------------------------------------
    def form_handling(self,pk,form:LeadFileForm,user):
        file = form.save(commit=False)
        file.team = self._get_team(user)
        file.lead_id = pk
        file.created_by = user
        file.save()
        
    # ------------------------------
    def _get_team(self, user):
        return Team.objects.filter(Q(created_by=user)|Q(members__id = user.id)).first()
