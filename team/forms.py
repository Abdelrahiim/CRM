from django import forms 
from team.models import Team

class TeamEditForm(forms.ModelForm):
    
    class Meta:
        
        model = Team
        fields = ['name','members']