"""
Models that will be used in the music school management system.
"""

from django.db import models

from lessons.models import Term
from lessons.models import User

# more needs to be added
"""
The School model holds shared state for a particular school.
"""
class School(models.Model):
    name = models.CharField(max_length=30, blank=False)
    director = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False
    )
    current_term = models.ForeignKey(
        Term,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
