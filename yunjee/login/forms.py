from django import forms
from .models import Account

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['nickname','introduction', 'profile_photo']