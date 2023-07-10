from django import forms 
from team.models import Team
from django.contrib.auth.models import User

class TeamEditForm(forms.ModelForm):
    
    class Meta:
        
        model = Team
        fields = ['name','members']
    
    name = forms.CharField(label="",widget= forms.TextInput(attrs={
        "class":"w-full my-2 px-6 py-4 bg-gray-200 rounded-xl"
    }))
    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            "class":"my-2  px-6 py-4 bg-gray-200 rounded-xl"
            }),
    )