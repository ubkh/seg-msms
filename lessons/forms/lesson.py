"""
Forms that will be used in the music school management system.
"""

from xml.dom import ValidationErr
from django import forms
from django.db.models import Q

from lessons.models import Lesson, User, Term, School

from datetime import datetime


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

    START_TYPES = [
        (0, 'By Term'),
        (1, 'By Date')
    ]

    start_type = forms.ChoiceField(choices=START_TYPES,
        label="Start",
        widget=forms.Select(attrs={
            'class': "form-select"
        })
    )

    class Meta:
        model = Lesson
        fields = ['fulfilled', 'start_date', 'start_term', 'end_date']
        widgets = {

        }
        labels = {}
    
    field_order = ['start_type', 'start_date', 'start_term', 'end_date']

    def clean(self):
        super().clean()
        if self.fields['end_date'] == None:
            if Term.objects.count() < 1:
                raise forms.ValidationError("End date cannot be blank if a term does not exist.")
                

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_term'].queryset = Term.objects.all()

        school_instance = School.objects.get(name="KCL Kangaroos")
        term = school_instance.get_update_current_term
        if term == None:
            self.fields.pop('start_term')
            self.fields.pop('start_type')
        
        # if term != None:
        #     # if mid-term
        #     if datetime.now().date() >= term.start_date and datetime.now().date() <= term.end_date:
        #         self.fields.pop('start_term')
        #     else:
        #         self.fields.pop('start_date')
        # else:
        #     self.fields.pop('start_term')