from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']

    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())