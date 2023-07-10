from django import forms

from leads.models import Lead ,Comment ,LeadFile

# ---------------------------------------------------------------
class LeadForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = Lead
        fields = ('name','email','description','status','priority')
    
    name = forms.CharField(label='',widget=forms.TextInput(attrs={
        'placeholder':"Lead Name",
        "class":"w-full px-6 py-4  bg-gray-200 rounded-xl"
    }))
    email = forms.EmailField(label='',widget=forms.EmailInput(attrs={
        'placeholder':"Lead Email",
        "class":"w-full px-6 py-4  bg-gray-200 rounded-xl"
    }))
    description = forms.CharField(label='',widget=forms.Textarea(attrs={
        'placeholder':"Lead Description",
        "class":"w-full px-6 py-4 bg-gray-200 rounded-xl"
    }))
    


# ---------------------------------------------------------------
class CommentForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = Comment
        fields = ('content',)
        
    content = forms.CharField(label="",widget=forms.Textarea(
        attrs={
            "placeholder" :"Enter Your Comment",
            "class":"w-full my-2 px-6 py-4 bg-gray-200 rounded-xl"
        }
    ))
    

class LeadFileForm(forms.ModelForm):
    
    # ------------------------------
    class Meta:
        model = LeadFile
        fields = ('file',)
        
    file = forms.FileField(widget=forms.FileInput({
        "placeholder":"Find File",
        "class":" py-2 px-5 my-5 w-full rounded-xl bg-gray-200"

    }))
    

