"""
Models that will be used in the music school management system.
"""

from django.db import models

from lessons.models import User, Lesson


class Transfer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=False)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
