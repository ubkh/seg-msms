"""
Forms that will be used in the music school management system.
"""

from django import forms
from django.db.models import Q

from lessons.models import Lesson, User


class LessonModifyForm(forms.ModelForm):
    """
    Model form used for students who wish to request a new lesson or change their preferences
    for an existing lesson request.
    """

    class Meta:
        model = Lesson
        fields = ['title', 'instrument', 'day', 'time', 'number_of_lessons', 'interval', 'duration', 'information']
        widgets = {
            'instrument': forms.Select(attrs={'class': "form-select"}),
            'day': forms.Select(attrs={'class': "form-select"}),
            'time': forms.TimeInput(format='%H:%M', attrs={
                'class': "form-control timepicker",
                'type': 'time'
            }),
            'number_of_lessons': forms.TextInput(attrs={
                'class': "form-control",
                'type': 'number',
                'min': '1'
            }),
            'interval': forms.TextInput(attrs={
                'class': "form-control",
                'type': 'number',
                'max': '4',
                'min': '1'
            }),
            'duration': forms.TextInput(attrs={
                'class': "form-control",
                'type': 'number',
                'max': '120',
                'min': '30',
                'step': '15'
            }),
            'title': forms.TextInput(attrs={'class': "form-control"}),
            'information': forms.Textarea(attrs={'class': "form-control"})
        }

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)


class LessonRequestForm(LessonModifyForm):
    class Meta(LessonModifyForm.Meta):
        model = Lesson
        fields = ['student'] + LessonModifyForm.Meta.fields
        LessonModifyForm.Meta.widgets |= {
            'student': forms.Select(attrs={'class': "form-select"})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(LessonRequestForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(Q(id=self.user.id) | Q(parent=self.user))
        self.fields['student'].empty_label = None

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
