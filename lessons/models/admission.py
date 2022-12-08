"""
Admission model that will be used in the music school management system.
"""

from django.contrib.auth.models import Group
from django.db import models


class Admission(models.Model):
    """
    Admission models that associates a user with a school and contains information about a users group with in a
    school.
    """
    
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    client = models.ForeignKey('User', on_delete=models.CASCADE, related_name='admission')
    groups = models.ManyToManyField(Group)
    is_active = models.BooleanField(default=True, verbose_name='Active Account')

    class Meta:
        unique_together = ('school', 'client')
