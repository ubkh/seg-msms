"""
Models that will be used in the music school management system.
"""

from audioop import reverse

from django.db import models
from django.utils import timezone

from lessons.models import User

DAYS_OF_WEEK = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
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
    day = models.IntegerField(choices=DAYS_OF_WEEK, default=0)
    hour = models.TimeField(default=timezone.now)
    number_of_lessons = models.IntegerField(default=1)
    interval = models.IntegerField()
    duration = models.IntegerField()
    title = models.TextField(max_length=20, default="Title")
    information = models.TextField(max_length=280)  # we can add more later
    price = models.FloatField(default=0.00)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('modify_lesson', kwargs=[self.id])
