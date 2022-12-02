from django.db import models

from lessons.models import User


class School(models.Model):
    name = models.CharField(max_length=30, blank=False)

    director = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False
    )
