"""
Forms that will be used in the music school management system.
"""

from django import forms
from django.core.validators import RegexValidator
from lessons.models import User

class RegisterForm(forms.ModelForm):
    """
    Model form used to register new users.
    """
    class Meta:
        model = User
        fields = ['name', 'email']

    password = forms.CharField(
        label='Password', 
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}$',
            message="Password must contain at least 6 characters, which includes "
                    "a uppercase character, a lowercase character and a number."
            )]
        )
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def clean(self):
        """
        Check if the data in the registration form is valid.
        """
        super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('password', 'The passwords do not match!')

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

class LoginForm(forms.Form):
    name = forms.CharField(label="name")
    email = forms.CharField(label="email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
