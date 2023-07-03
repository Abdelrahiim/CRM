from django import forms

from leads.models import Lead

class AddLeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ('name','email','description','status','priority')


