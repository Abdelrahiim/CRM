from django.db import models
from CRM.nano_id_function import get_nano_id
from django.contrib.auth.models import User


# ---------------------------------------------------------------
class Lead(models.Model):
    LOW = 'low'
    HIGH = 'high'
    MEDIUM = 'medium'
    NEW ='new'
    CONTACTED='contacted'
    WON = 'won'
    LOST = 'low'

    CHOICES_PRIORITY = (
        (LOW,'Low'),
        (HIGH,'High'),
        (MEDIUM,'Medium'),
    )
    CHOICES_STATUS = (
        (NEW,'New'),
        (CONTACTED,'Contacted'),
        (WON,'Won'),
        (LOST,'Lost'),
    )
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    name= models.CharField(max_length=50)
    email = models.EmailField()
    description= models.TextField(blank=True,null=True)
    convert_to_client = models.BooleanField(default=False)
    priority = models.CharField(max_length=10,choices=CHOICES_PRIORITY,default=MEDIUM)
    status = models.CharField(max_length=12,choices=CHOICES_STATUS,default=NEW)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='leads')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    # ------------------------------
    def __str__(self) -> str:
        return self.name