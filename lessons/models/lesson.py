"""
Lesson model that will be used in the music school management system.
"""
from django.apps import apps
from django.urls import reverse

from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator, StepValueValidator
from lessons.models import User
from lessons.models.term import Term

DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]

INSTRUMENTS = [
    ('Piano', 'Piano'),
    ('Guitar', 'Guitar'),
    ('Drums', 'Drums'),
    ('Violin', 'Violin'),
    ('Trumpet', 'Trumpet'),
    ('Flute', 'Flute'),
    ('Harp', 'Harp'),
]

START_TYPES = [
    ('Term', 'By Term'),
    ('Date', 'By Date')
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
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        blank=False
    )
    day = models.TextField(choices=DAYS_OF_WEEK, default='Monday')
    instrument = models.TextField(choices=INSTRUMENTS, default='Piano')
    teacher = models.ForeignKey(
        User,
        related_name='teacher',
        blank=False,
        on_delete=models.CASCADE,
        default=''
    )
    time = models.TimeField(default=timezone.now)
    number_of_lessons = models.PositiveIntegerField(
        default=1,
        verbose_name="Number of Lessons",
        validators=[MinValueValidator(1)]
    )
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
    title = models.CharField(max_length=25, default="Music Lesson", )
    information = models.CharField(max_length=280, verbose_name="Further Information", blank=True)
    price = models.DecimalField(default=10.00, max_digits=10, decimal_places=2, validators=[MinValueValidator(5.00)])
    start_type = models.TextField(choices=START_TYPES, default='Term')
    start_term = models.ForeignKey(
        Term,
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    @property
    def total_paid(self):
        """
        Calculate the total paid amount of all transfers that relate to this lesson.
        """
        transfer_list = apps.get_model('lessons.Transfer').objects.filter(lesson=self.id)
        total_paid = 0
        for transfer in transfer_list:
            total_paid += transfer.amount
        return total_paid

    @property
    def payment_status(self):
        """
        Return a suitable status message of the paid amount of a transfer.
        """
        if self.total_paid == 0:
            return "Unpaid"
        elif self.total_paid < self.price:
            return "Partially Paid"
        elif self.total_paid == self.price:
            return "Paid"
        elif self.total_paid > self.price:
            return "Overpaid"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('booking_invoice', kwargs=[self.id])


class ScheduledLesson(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        blank=False,
        on_delete=models.CASCADE  # check this
    )
    start = models.DateTimeField(blank=False)
    end = models.DateTimeField(blank=False)
