"""
Models that will be used in the music school management system.
"""

from django.db import models
from django.urls import reverse


class Term(models.Model):
    """
    The Term date specifies a start and end date for a corresponding school.
    """

    start_date = models.DateField()
    end_date = models.DateField()
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        blank=False
    )

    class Meta:
        ordering = ['start_date', ]

    def __str__(self):
        return "Term " + str(self.id)

    def get_absolute_url(self):
        return reverse('edit_term', kwargs=[self.id])