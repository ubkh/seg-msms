"""
Forms that will be used in the music school management system.
"""

from django import forms
from django.core.validators import RegexValidator
from lessons.models import User, Lesson, Transfer

"""
Authentication Forms
"""


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
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            password=self.cleaned_data.get('password')
        )
        return user

class LoginForm(forms.Form):
    email = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

class AdminModifyForm(forms.ModelForm):
    """
    Model form to modify an existing administrator by a director.
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    make_account_director = forms.BooleanField(
        label="Would you like to make this account a director account?",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-label'})
    )
    delete_account = forms.BooleanField(label="Would you like to delete this account?", required=False)


"""
Lessons Forms
"""


class LessonRequestForm(forms.ModelForm):
    """
    Model form used for students to request new lessons.
    """
    class Meta:
        model = Lesson
        fields = ['day', 'hour', 'number_of_lessons', 'interval', 'duration', 'title', 'information']

    hour = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)
  
class LessonModifyForm(forms.ModelForm):
    """
    Model form for students who wish to change preferences for a lesson request.
    """
    class Meta:
        model = Lesson
        fields = ['day', 'hour', 'number_of_lessons', 'interval', 'duration', 'title', 'information']

    hour = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)

class LessonFulfillForm(forms.ModelForm):
    """
    Model form for administrators who wish to fulfill a booking.
    """
    class Meta:
        model = Lesson
        fields = ['fulfilled']

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


"""
Transfer Form
"""


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['lesson', 'user', 'amount']

    lesson = forms.IntegerField()
    user = forms.IntegerField()
