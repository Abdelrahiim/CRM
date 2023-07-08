from django.db import models
from CRM.nano_id_function import get_nano_id
from django.contrib.auth.models import User
from team.models import Team

# ---------------------------------------------------------------
class Client(models.Model):
    """
    Client Table
    """
    id = models.CharField(max_length=12, primary_key=True, null=False, unique=True, default=get_nano_id)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client')
    team = models.ForeignKey(Team,related_name='clients_team',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    # -----------------------
    def __str__(self):
        return self.name
    