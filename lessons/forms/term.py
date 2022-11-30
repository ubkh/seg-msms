"""
Forms that will be used in the music school management system.
"""

from django import forms

from lessons.models import Term

class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': "form-control",
                'type': 'date',
            }),
            'end_date': forms.DateInput(attrs={
                'class': "form-control",
                'type': 'date',
            })
        }
    
    def clean(self):
        cleaned = super(TermForm, self).clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        conflicts = Term.objects.filter(
            start_date__lte=end,
            end_date__gte=start
        )
        if any(conflicts):
            raise forms.ValidationError("These dates overlap with existing terms.")
        if end <= start:
            raise forms.ValidationError("The end date cannot be earlier or equal to the start date!")
        return cleaned
