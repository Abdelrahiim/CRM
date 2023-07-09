from django import forms

from client.models import Client,ClientComment,ClientFile


# ---------------------------------------------------------------
class ClientForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = Client
        fields = ('name','email','description')
        

# ---------------------------------------------------------------
class CommentForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = ClientComment
        fields = ('content',)
    
    
class ClientFileForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = ClientFile
        fields = ('file',)