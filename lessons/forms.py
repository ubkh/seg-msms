"""
Forms that will be used in the music school management system.
"""

from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    """
    Model form used to register new users.
    """
    class Meta:
        model = User
        fields = ['name', 'email']

    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def save(self):
        """
        Save the user's registration details on to a database.
        """
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('email'),
            name=self.cleaned_data.get('name'),
            password=self.cleaned_data.get('password')
        )
        return user
