from django import forms
from .models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email']

    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput())

    def save(self):
        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('email'),
            name=self.cleaned_data.get('name'),
            password=self.cleaned_data.get('password')
        )
        return user