from django import forms
from django.contrib.auth.models import User
from MECboard.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

class ProfileForm(forms.ModelForm): # form과 모델form은 수동과 자동
    class Meta:
        model = Profile
        fields = ['nickname','introduction', 'profile_photo']
