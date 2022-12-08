"""
Forms that will be used in the music school management system.
"""

from django import forms
from django.db.models import Q

from lessons.models import Term

class TermForm(forms.ModelForm):
    """
    Model form used to create term dates.
    """

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
        """
        Validate that data in the term form is correct.
        """

        cleaned = super(TermForm, self).clean()
        start = cleaned.get('start_date')
        end = cleaned.get('end_date')
        conflicts = Term.objects.filter(
            school_id=self.school,
            start_date__lte=end,
            end_date__gte=start
        )
        # we are editing a term in this case
        if self.term:
            # remove this term from conflicts as we are editing it
            conflicts = conflicts.filter(~Q(id=self.term.id))
        if any(conflicts):
            raise forms.ValidationError("These dates overlap with existing terms.")
        if end <= start:
            raise forms.ValidationError("The end date cannot be earlier or equal to the start date!")
        return cleaned

    def __init__(self, *args, **kwargs):
        self.school = kwargs['initial']['school']
        self.term = kwargs['instance']
        super(TermForm, self).__init__(*args, **kwargs)