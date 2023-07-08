from django.shortcuts import render
from django.views import View, generic
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin


# ---------------------------------------------------------------
class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = "index.html"


# ---------------------------------------------------------------
class AboutView(LoginRequiredMixin, generic.TemplateView):
    template_name = "about.html"
