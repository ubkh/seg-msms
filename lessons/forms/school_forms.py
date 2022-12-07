from django import forms

from lessons.models import School


class SchoolCreateForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
        }


class SchoolManageForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
        }

    delete_school = forms.BooleanField(
        label="Do you want to delete this School?",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': "form-check-input"})
    )
