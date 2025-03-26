from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserBioForm(forms.Form):
    name = forms.CharField(max_length=10)
    age = forms.IntegerField(label="How old are you", min_value=1, max_value=120)
    bio = forms.CharField(label="Biography", widget=forms.Textarea)
    
    
    
def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and "virus" in file.name:
        raise ValidationError("File name shouldn't contain 'virus'")

class UploadFileForm(forms.Form):
    myfile = forms.FileField(validators=[validate_file_name,])
