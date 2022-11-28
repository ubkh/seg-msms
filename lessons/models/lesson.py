"""
Models that will be used in the music school management system.
"""

from django.urls import reverse

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, StepValueValidator
from lessons.models import User

DAYS_OF_WEEK = [
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday'),
    ('Sunday','Sunday'),
]


class Lesson(models.Model):
    """
    Lesson model used to represent a fulfilled or unfulfilled lesson.
    """
    fulfilled = models.BooleanField(default=False)
    student = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE
    )
    day = models.TextField(choices=DAYS_OF_WEEK, default='Monday')
    time = models.TimeField(default=timezone.now)
    number_of_lessons = models.PositiveIntegerField(default=1, verbose_name="Number of Lessons")
    interval = models.PositiveIntegerField(
        default=1, 
        validators=[MinValueValidator(1), MaxValueValidator(4)],
        verbose_name="Interval (weeks)"
    )
    duration = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(30), MaxValueValidator(60), StepValueValidator(15)],
        verbose_name="Duration (minutes)"
    )
    title = models.TextField(max_length=25, default="Music Lesson")
    information = models.TextField(max_length=280, verbose_name="Further Information", blank=True)
    price = models.DecimalField(default=0.00,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('booking_invoice', kwargs=[self.id])
