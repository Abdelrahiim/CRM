from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from client.models import Client
from client.forms import AddClientForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

# Create your views here.


# -------------------------------------------------------------
class ClientList(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request):
        clients = Client.objects.all()
        return render(request, "clients\clients.html", {"clients": clients})


# -------------------------------------------------------------
class SingleClient(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        client = get_object_or_404(Client, created_by=request.user, pk=pk)
        return render(request, "clients/single_client.html", {"client": client})


# -------------------------------------------------------------
class CreateNewCLient(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request):
        form = AddClientForm()
        return render(request, "clients/create-client.html", {"form": form})

    # ------------------------------
    def post(self, request):
        form = AddClientForm(request.POST)
        if form.is_valid():
            self._create_client(request, form)
            return redirect("clients")

        raise ValidationError("Error Validate The Form")

    # ------------------------------
    def _create_client(self, request, form: AddClientForm):
        client = form.save(commit=False)
        client.created_by = request.user
        client.save()
        messages.success(request, "Client Created Successfully")


class UpdateClient(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        form = AddClientForm()
        return render(request, "clients/client-edit.html", {"form": form})

    # ------------------------------
    def post(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        client = get_object_or_404(Client, created_by=request.user, pk=pk)
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "The Client Was edited Successfully")
            return redirect("clients")


class DeleteClient(LoginRequiredMixin, View):
    
    # ------------------------------
    def get(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        self._delete_client(request, pk)
        return redirect("clients")

    # ------------------------------
    def _delete_client(self, request, pk):
        client = get_object_or_404(Client, created_by=request.user, pk=pk)
        client.delete()
        messages.success(request, "Client Deleted Successfully")
