from django import forms

from lessons.models import School


class SchoolCreateForm(forms.ModelForm):
    """
    Model form used to create new schools
    """

    class Meta:
        model = School
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
        }


class SchoolManageForm(forms.ModelForm):
    """
    Model form used to modify or delete a schools
    """

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
