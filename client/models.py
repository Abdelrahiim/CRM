from django.db import models
from CRM.custom_config import get_nano_id ,unique_filename
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
    
    class Meta:
        ordering = ('-modified_at',)
    # -----------------------
    def __str__(self):
        return self.name
    

# ---------------------------------------------------------------
class ClientFile(models.Model):
    """
    CLient File Table
    
    """
    
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    team = models.ForeignKey(Team,related_name='clients_files_team',on_delete=models.CASCADE)
    client = models.ForeignKey(Client,related_name="clients_files",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='clients_files_user')
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True,null=True,upload_to=unique_filename("clients_files"))
    
    



# ---------------------------------------------------------------
class ClientComment(models.Model):
    """
    Client Comment Table
    
    """
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    team = models.ForeignKey(Team,related_name='comments_client_team',on_delete=models.CASCADE)
    client = models.ForeignKey(Client,related_name="comments",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments_client_user')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True,null=True)

    def __str__(self) -> str:
        return self.created_by.username