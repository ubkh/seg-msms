"""
Models that will be used in the music school management system.
"""
from django.db import models
from datetime import datetime
from django.utils.text import slugify

from lessons.models import Term
from lessons.models import User
from lessons.models.mixins import AdmissionMixin


# more needs to be added


class School(AdmissionMixin, models.Model):
    """
    The School model holds shared state for a particular school.
    """
    name = models.CharField(max_length=30, blank=False)
    slug = models.SlugField(unique=True, default=name)
    director = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=False,
        related_name='managed_school'
    )
    current_term = models.ForeignKey(
        Term,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    clients = models.ManyToManyField(
        User,
        through='Admission',
        related_name='enrolled_school'
    )
    description = models.TextField(max_length=1000)

    @property
    def get_update_current_term(self):
        if self.current_term:
            if datetime.now().date() > self.current_term.end_date:
                next = Term.get_next_by_start_date(self.current_term)
                self.current_term = next
        return self.current_term

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(AdmissionMixin, self).save(*args, **kwargs)

    def __str__(self):
        return str(f"{self.name}")
