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
        fields = ['first_name', 'last_name', 'email']

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
    make_account_adult_student = forms.BooleanField(
        label="Would you like to make this account an adult account?",
        required=False
    )

    def clean(self):
        """
        Check if the data in the registration form is valid.
        """
        super().clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
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
            password=self.cleaned_data.get('password')
        )
        return user


class LoginForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class EditUserForm(forms.ModelForm):
    """
    Model form to modify an existing administrator by a director.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AdminModifyForm(forms.ModelForm):
    """
    Model form to modify an existing administrator by a director.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    make_account_super_administrator = forms.BooleanField(
        label="Would you like to make this account a super administrator account?",
        required=False
    )
    delete_account = forms.BooleanField(
        label="Would you like to delete this account?",
        required=False
    )


class ChildCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ManageMemberForm(forms.Form):
    client = forms.BooleanField(required=False)
    teacher = forms.BooleanField(required=False)
    administrator = forms.BooleanField(required=False)
    super_administrator = forms.BooleanField(required=False)
    ban_member = forms.BooleanField(required=False)


class BanClientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']


class TeacherRegisterForm(forms.ModelForm):
    """
    Model form used to register new teachers.
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
            message="Password must contasin at least 6 characters, which includes "
                    "a uppercase character, a lowercase character and a number."
        )]
    )
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': "form-control"}))


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
        Save the teacher's registration details on to a database.
        """
        super().save(commit=False)
        teacher = User.objects.create_teacher(
            self.cleaned_data.get('email'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            instrument=self.cleaned_data.get('instrument'),
            password=self.cleaned_data.get('password')
        )
        return teacher

