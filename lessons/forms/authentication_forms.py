"""
Forms relating to authentication that will be used in the music school management system.
"""

from django import forms
from django.core.validators import RegexValidator

from lessons.models import User


class RegisterForm(forms.ModelForm):
    """
    Model form used to register new users, whether students, teachers or administrators.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'instrument']
        widgets = {
            'title': forms.Select(attrs={'class': "form-select"}),
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'instrument': forms.CheckboxSelectMultiple()
        }

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': "form-control"}),
        validators=[RegexValidator(
            regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{6,}$',
            message="Password must contain at least 6 characters, which includes "
                    "a uppercase character, a lowercase character and a number."
        )]
    )
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': "form-control"}))
    make_account_adult_student = forms.BooleanField(
        label="Would you like to make this account an adult account?",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input"})
    )

    def clean(self):
        """
        Validate that data in the registration form is correct, if not display an error.
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
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            instrument=self.cleaned_data.get('instrument'),
            password=self.cleaned_data.get('password')
        )
        return user


class LoginForm(forms.Form):
    """
    Model form used to log in a registered user.
    """

    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': "form-control"}))


class EditUserForm(forms.ModelForm):
    """
    Model form to modify or delete an existing user.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'instrument']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'instrument': forms.CheckboxSelectMultiple()
        }

    delete_account = forms.BooleanField(
        label="Would you like to delete this account?",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input"})
    )


class ChildCreateForm(forms.ModelForm):
    """
    Model form to create a child for an existing adult user.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
        }


class ManageMemberForm(forms.Form):
    """
    Form to create manage member permissions and groups with in a specific school.
    """

    client = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    teacher = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    administrator = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    super_administrator = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input"})
    )
    ban_member = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
