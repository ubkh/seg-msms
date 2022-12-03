"""
Models that will be used in the music school management system.
"""

from django.db import models

class Term(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        ordering = ['start_date', ]

    #def __str__(self):
        