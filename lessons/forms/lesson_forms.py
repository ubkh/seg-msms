"""
Forms that will be used in the music school management system.
"""

from django import forms
from django.db.models import Q
from django.shortcuts import get_object_or_404

from lessons.models import Lesson, User, Term, School


class LessonModifyForm(forms.ModelForm):
    """
    Model form used for students who wish to modify a lesson
    """
    
    teacher = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={'class': "form-select"}),
        )

    class Meta:
        model = Lesson
        fields = ['title', 'instrument', 'number_of_lessons', 'teacher', 'day', 'time', 'interval', 'duration', 'information']
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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.school = kwargs.pop('school')
        super(LessonModifyForm, self).__init__(*args, **kwargs)
        school_users = User.objects.filter(
            Q(enrolled_school=self.school)
            & Q(admission__groups__name='Teacher')
            & ~Q(id=self.user.id))
        self.fields['teacher'].queryset = school_users
        if not school_users.count():
            self.fields['teacher'].empty_label = "There are no teachers available."
        else:
            self.fields['teacher'].empty_label = "Select a teacher."


    def form_valid(self, form):
        """
        Check if the data in the modify lesson form is valid.
        """
        form.instance.student = self.request.user
        return super().form_valid(form)


class LessonRequestForm(LessonModifyForm):
    """
    Model form used for students who wish to request a new lesson
    """

    class Meta(LessonModifyForm.Meta):
        model = Lesson
        fields = ['student'] + LessonModifyForm.Meta.fields
        LessonModifyForm.Meta.widgets |= {
            'student': forms.Select(attrs={'class': "form-select"})
        }

    def __init__(self, *args, **kwargs):
        super(LessonRequestForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(Q(id=self.user.id) | Q(parent=self.user))
        self.fields['student'].empty_label = None


    def form_valid(self, form):
        """
        Check if the data in the request lesson form is valid.
        """
        form.instance.student = self.request.user
        return super().form_valid(form)


class LessonFulfillForm(forms.ModelForm):
    """
    Model form for administrators who wish to fulfill a booking.
    """
    class Meta:
        model = Lesson
        fields = ['day', 'time', 'number_of_lessons', 'duration', 'interval', 'start_type', 'start_date', 'start_term', 'end_date']
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
        """
        Validate that data in the term form is correct. If an errors occurs, return what went wrong.
        """
        super().clean()
        start_type = self.cleaned_data.get('start_type')
        if start_type != None:
            if start_type=="Date" and self.fields['start_date'].initial == None:
                raise forms.ValidationError("Start date cannot be blank!")
                
        if self.fields['end_date'] == None:
            print(self.data)
            if Term.objects.filter(school_id=self.data['school']).count() < 1:
                raise forms.ValidationError("End date cannot be blank if a term does not exist.")
                

    def form_valid(self, form):
        """
        Check if the data in the fullfilled lesson form is valid.
        """
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
        
