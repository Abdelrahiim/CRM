from django.db import models
from django.contrib.auth.models import User
from CRM.custom_config import get_nano_id
from team.models import Team

# Create your models here.

# ---------------------------------------------------------------
class UserProfileModel(models.Model):
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    user = models.OneToOneField(User,related_name="user_profile",on_delete=models.CASCADE)
    active_team = models.ForeignKey(Team,related_name='user_profile',blank=True,null=True,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username