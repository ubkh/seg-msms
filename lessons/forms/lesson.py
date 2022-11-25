"""
Forms that will be used in the music school management system.
"""

from django import forms

from lessons.models import Lesson


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
