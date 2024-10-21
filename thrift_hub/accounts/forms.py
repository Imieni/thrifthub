from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address', 'state', 'username', 'password', 'profile_picture']


class LoginForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'password']