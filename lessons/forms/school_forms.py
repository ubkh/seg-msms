from django import forms

from lessons.models import School


class SchoolCreateForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name']


class SchoolManageForm(forms.Form):
    join_school = forms.BooleanField(required=False)
