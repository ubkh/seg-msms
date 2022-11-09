"""Models that will be used in the music school management system."""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import EmailValidator, RegexValidator

# Create your models here.

class UserManager(BaseUserManager):
    """User manager used to create new users."""
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """Create a generic user according to its attributes."""
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
        """Create a standard user."""
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create a super user."""
        return self._create_user(email, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """User model used for authentication."""
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
            regex=r'^(?:[^\W\d_]|-|\s)+$'
        )]
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
