from django import forms

from lessons.models import School


class SchoolCreateForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'description']


class SchoolManageForm(forms.Form):
    join_school = forms.BooleanField(required=False)


class SchoolDeleteForm(forms.ModelForm):

    class Meta:
        model = School
        exclude = ['name', 'director', 'current_term']

    delete_school = forms.BooleanField(
        label="Do you want to delete this School?",
        required=False
    )
