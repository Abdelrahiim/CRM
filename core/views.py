from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

# ---------------------------------------------------------------
class IndexView(LoginRequiredMixin,View):
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        return render(request,'index.html')
    
    

# ---------------------------------------------------------------
class AboutView(View):
    
    # ------------------------------
    def get(self,request,*args, **kwargs):
        return render(request,'about.html')
    
