"""
User model that will be used in the music school management system to authenticate clients.
"""

import re

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator
from django.db import models
from multiselectfield import MultiSelectField

from lessons.models.mixins import GroupRegistrationMixin


INSTRUMENTS = [
    ('Piano', 'Piano'),
    ('Guitar', 'Guitar'),
    ('Drums', 'Drums'),
    ('Violin', 'Violin'),
    ('Trumpet', 'Trumpet'),
    ('Flute', 'Flute'),
    ('Harp', 'Harp'),
]

class UserManager(BaseUserManager):
    """
    User manager used to create new users.
    """

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
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


class User(PermissionsMixin, GroupRegistrationMixin, AbstractBaseUser):
    """
    User model used for authentication.
    """
    
    email = models.EmailField(
        verbose_name="Email",
        max_length=254,
        null=True,
        blank=False,
        unique=True,
        validators=[EmailValidator(
            message="Please enter a valid e-mail!",
            code='invalid'
        )]
    )
    first_name = models.CharField(
        verbose_name="First name",
        max_length=40,
        blank=False,
        validators=[RegexValidator(
            message="Please enter a valid name!",
            regex=re.compile(r'^(?:[a-zA-ZÀ-ž]|-|\s)+$', re.UNICODE)
        )]
    )
    last_name = models.CharField(
        verbose_name="Last name",
        max_length=40,
        blank=False,
        validators=[RegexValidator(
            message="Please enter a valid name!",
            regex=re.compile(r'^(?:[a-zA-ZÀ-ž]|-|\s)+$', re.UNICODE)
        )]
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )
    is_staff = models.BooleanField(default=False)
    instrument = MultiSelectField(
        verbose_name="Interested in teaching? Select the following instruments that could be taught.",
        max_length=1000,
        choices=INSTRUMENTS,
        null=False,
        blank=True
    )
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name='Active Account')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return str(f"{self.first_name} {self.last_name}")
