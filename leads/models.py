from django.db import models
from CRM.custom_config import get_nano_id,unique_filename
from django.contrib.auth.models import User

from team.models import Team



# ---------------------------------------------------------------
class Lead(models.Model):
    """
    Lead Table
    
    """
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
    team = models.ForeignKey(Team,related_name='leads_team',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    # ------------------------------
    def __str__(self) -> str:
        return self.name


# ---------------------------------------------------------------
class LeadFile(models.Model):
    """
    Lead File Table
    
    """
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    team = models.ForeignKey(Team,related_name='lead_files_team',on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead,related_name="lead_files",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='lead_files_user')
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=unique_filename("lead_files"))
    
    


# ---------------------------------------------------------------
class Comment(models.Model):
    """
    Lead Comment Table
    
    """
    
    id = models.CharField(max_length=12,primary_key=True,null=False,unique=True,default=get_nano_id)
    team = models.ForeignKey(Team,related_name='comments_team',on_delete=models.CASCADE)
    lead = models.ForeignKey(Lead,related_name="comments_lead",on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_user')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=True,null=True)

    # ------------------------------
    def __str__(self) -> str:
        return self.created_by.username
