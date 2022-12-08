"""
Transfer form that will be used in the music school management system.
"""
import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from lessons.models import User, Lesson, Transfer, School


class TransferForm(forms.ModelForm):
    """
    Transfer form records transactions made by the user to pay for lessons. An administrator of a school will enter a
    transaction, and it will be recorded for that school.
    """

    class Meta:
        model = Transfer
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={
                'class': "form-control",
                'type': 'number',
                'min': '0'
            }),
        }

    def __init__(self, school, *args, **kwargs):
        self.school = school
        self.transfer_pattern = re.compile(r'^[0-9]+-[0-9]+$')
        super(TransferForm, self).__init__(*args, **kwargs)

    transfer_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"}),
        validators=[RegexValidator(
            regex=re.compile(r'^[0-9]+-[0-9]+$'),
            message="Transfer reference must be in the format XXXX-YYYY where X is the user reference number and Y is "
                    "the invoice reference number.",
        )]
    )

    def clean(self):
        """
        Validate that data in the transfer form is correct. If an errors occurs return what went wrong.
        """
        cleaned_data = super(TransferForm, self).clean()
        transfer_number = str(self.cleaned_data.get('transfer_id'))

        if not re.fullmatch(self.transfer_pattern, transfer_number):
            raise ValidationError(message="")

        user_id, invoice_id = re.split(r'\D+', transfer_number)

        user = User.objects.filter(pk=user_id).first()
        lesson = Lesson.objects.filter(pk=invoice_id).first()
        if user and lesson:
            if user != lesson.student:
                self.add_error('transfer_id', 'This student has not booked this lesson. You should refund this '
                                              'transfer.')
            else:
                if not lesson.fulfilled:
                    self.add_error('transfer_id', "This lesson has not been fulfilled yet.")
                if lesson.school.id != self.school:
                    self.add_error('transfer_id', "This lesson is not managed by this school")
        if not user:
            self.add_error('transfer_id', 'This user could not be found. You should refund this transfer.')
        if not lesson:
            self.add_error('transfer_id', 'This lesson could not be found. You should refund this transfer.')
        return cleaned_data

    def save(self):
        """
        Save the transfer onto the database.
        """
        super().save(commit=False)
        transfer_number = str(self.cleaned_data.get('transfer_id'))
        user_id, invoice_id = re.split(r'\D+', transfer_number)
        transfer = Transfer.objects.create(
            user=User.objects.get(pk=user_id),
            lesson=Lesson.objects.get(pk=invoice_id),
            school=School.objects.get(pk=self.school),
            amount=self.cleaned_data.get('amount')
        )
        return transfer
