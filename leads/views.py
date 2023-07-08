from typing import Any, Dict
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.forms import AddLeadForm
from leads.models import Lead
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponse
from client.models import Client
from team.models import Team

# --------------------------------------------------------------
class ListAllLeads(LoginRequiredMixin, View):
    template_name = "leads/leads.html"

    # ------------------------------
    def get(self, request, *args, **kwargs):
        leads = Lead.objects.filter(created_by=request.user, convert_to_client=False)
        return render(request, self.template_name, {"leads": leads})


# --------------------------------------------------------------
class SingleLead(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        return render(request, "leads/single_lead.html", {"lead": lead})

# --------------------------------------------------------------
class AddLeadView(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = AddLeadForm()
        team = self._get_team(request.user)
        return render(request, "leads/create_lead.html", {"form": form,"team":team})
    
    # ------------------------------
    def post(self, request, *args, **kwargs):
        form = AddLeadForm(request.POST)

        if form.is_valid():
            self._create_lead(request, form)

            return redirect("leads_list")

        raise ValidationError("Error Validate The Form")
    
    # ------------------------------
    def _create_lead(self, request, form: AddLeadForm):
        lead = form.save(commit=False)
        lead.created_by = request.user
        lead.team = self._get_team(request.user)

        lead.save()
        messages.success(request, "The Lead Was Created Successfully")

    # ------------------------------
    def _get_team(self,user):
        team =  Team.objects.filter(created_by=user).first()
        print(len(team.leads_team.all()))
        return team
        


# --------------------------------------------------------------
class UpdateLead(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = AddLeadForm()
        return render(
            request, "leads/leads_edit.html", {"form": form, "pk": kwargs["pk"]}
        )

    # ------------------------------
    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        form = AddLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "The Lead Was edited Successfully")
            return redirect("leads_list")


class DeleteLead(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        self._delete_lead(request,pk)
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
        self._update_lead(request.user, lead,team)
        messages.success(request, "Lead Is Converted To Client Successfully")
        return redirect("leads_list")

    # ------------------------------
    def _update_lead(self, user, lead,team):
        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=user,
            team = team
        )
        lead.convert_to_client = True
        lead.save()

    # ------------------------------
    def _get_team(self,user):
        return Team.objects.filter(created_by=user).first()