from django.db import models
from django.contrib.auth.models import User
from user_profile.models import UserProfileModel
from CRM.custom_config import get_nano_id


# ---------------------------------------------------------------
class Plan(models.Model):
    """
    Plan Table
    """
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2,max_digits=4)
    max_leads = models.IntegerField()
    max_client = models.IntegerField()
    
    # ------------------------------
    def __str__(self) -> str:
        return self.name
    

# ---------------------------------------------------------------
class Team(models.Model):
    """
    Team Table
    """
    
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User,related_name='teams')
    plan = models.ForeignKey(Plan,related_name='team_plan',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='created_team',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # ------------------------------
    def __str__(self) -> str:
        return self.name
    
    
