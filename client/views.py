from django.shortcuts import render, redirect
from django.views import View
from client.models import Client
# Create your views here.

class ClientList(View):
    
    def get(self,request):
        
        clients = Client.objects.all()
        return render(request,'clients\clients.html',{"clients":clients})