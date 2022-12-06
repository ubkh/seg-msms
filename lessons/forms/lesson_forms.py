"""
Forms that will be used in the music school management system.
"""

from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404

from lessons.models import Lesson, User, Term, School

from datetime import datetime


class LessonModifyForm(forms.ModelForm):
    """
    Model form used for students who wish to request a new lesson or change their preferences
    for an existing lesson request.
    """
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='Teacher'), widget=forms.Select(attrs={'class': "form-select"}), empty_label="Select a teacher")
    class Meta:
        model = Lesson
        fields = ['title', 'instrument', 'teacher', 'day', 'time', 'number_of_lessons', 'interval', 'duration', 'information']
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
        fields = ['day', 'time', 'duration', 'interval', 'number_of_lessons', 'start_type', 'start_date', 'start_term', 'end_date']
        widgets = {
           'day': forms.Select(attrs={'class': "form-select"}),
           'start_term': forms.Select(attrs={'class': "form-select"}),
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
            'start_date': forms.TextInput(attrs={
                'class': "form-control",
                'type': 'date'
            }),
            'end_date': forms.TextInput(attrs={
                'class': "form-control",
                'type': 'date'
            }),
            'start_type': forms.Select(attrs={
                'class': "form-select"
            })
        }
        labels = {
            'start_type': "Start"
        }
    
    field_order = ['start_type', 'start_date', 'start_term', 'end_date']

    def clean(self):
        super().clean()
        if self.fields['end_date'] == None:
            print(self.data)
            if Term.objects.filter(school_id=self.data['school']).count() < 1:
                raise forms.ValidationError("End date cannot be blank if a term does not exist.")
                

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_term'].queryset = Term.objects.filter(school_id=kwargs['initial']['school'])
        self.fields['start_term'].empty_label = None

        school_instance = get_object_or_404(School, pk=kwargs['initial']['school'])
        term = school_instance.get_update_current_term
        if term == None:
            self.fields.pop('start_term')
            self.fields.pop('start_type')
        
