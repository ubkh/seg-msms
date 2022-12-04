from django import forms

from lessons.models import School


class SchoolCreateForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']
