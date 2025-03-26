from django import forms
from .models import Profile, User

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        queryset = model.objects.prefetch_related('users').all()
        fields = ('user',  'bio', 'avatar',)