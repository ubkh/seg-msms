"""
Models that will be used in the music school management system.
"""
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from lessons.models import User, Lesson


class Transfer(models.Model):
    """
    ~
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        blank=False
    )
    amount = models.DecimalField(
        validators=[MinValueValidator(Decimal('0.01'))],
        max_digits=8,
        decimal_places=2
    )
