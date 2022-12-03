"""
Forms that will be used in the music school management system.
"""

from django import forms

from lessons.models import User, Lesson, Transfer, School


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = ['amount']

    user_id = forms.IntegerField()
    lesson_id = forms.IntegerField()

    def clean(self):
        super().clean()
        user_id = self.cleaned_data.get('user_id')
        user = User.objects.filter(pk=user_id).first()
        lesson_id = self.cleaned_data.get('lesson_id')
        lesson = Lesson.objects.filter(pk=lesson_id).first()
        if user and lesson and user != lesson.student:
            self.add_error('amount', 'This student has not booked this lesson. You should refund this transfer.')
        if not user:
            self.add_error('user_id', 'This user could not be found. You should refund this transfer.')
        if not lesson:
            self.add_error('lesson_id', 'This lesson could not be found. You should refund this transfer.')
