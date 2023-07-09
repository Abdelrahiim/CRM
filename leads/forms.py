from django import forms

from leads.models import Lead ,Comment ,LeadFile

# ---------------------------------------------------------------
class LeadForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = Lead
        fields = ('name','email','description','status','priority')


# ---------------------------------------------------------------
class CommentForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = Comment
        fields = ('content',)
    

class LeadFileForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = LeadFile
        fields = ('file',)
    

