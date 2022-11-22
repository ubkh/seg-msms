"""
Models that will be used in the music school management system.
"""

from audioop import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
import re

# Create your models here.

class UserManager(BaseUserManager):
    """
    User manager used to create new users.
    """
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Create a generic user according to its attributes.
        """
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email = self.normalize_email(email),
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """
        Create a standard user.
        """
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a super user.
        """
        return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    User model used for authentication.
    """
    email = models.EmailField(
        max_length=254, 
        blank=False, 
        unique=True, 
        validators=[EmailValidator(
            message="Please enter a valid e-mail!",
            code='invalid'
        )]
    )
    name = models.CharField(
        max_length=100, 
        blank=False,
        validators=[RegexValidator(
            message="Please enter a valid name!",
            regex=re.compile(r'^(?:[\u0530-\u19ff]|[^\W\d_]|-|\s)+$', re.UNICODE)
        )]
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

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
    price = models.FloatField(default=0.00)
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
    information = models.TextField(max_length=280) # we can add more later

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('modify_lesson', kwargs=[self.id])

class Transfer(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, blank=False)
    # Fix bug where only a user can only pay for a single lesson
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_constraint=False)
    amount = models.IntegerField()
