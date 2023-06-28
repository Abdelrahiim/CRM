from django.db import models
from django.contrib.auth.models import User
from nano_id_function import get_nano_id

# Create your models here.


class UserProfileModel(models.Model):
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    user = models.OneToOneField(User,related_name="user_profile",on_delete=models.CASCADE)
    