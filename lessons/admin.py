"""Configuration of the admin interface for the music school management system."""

from django.contrib import admin
from .models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface to display users."""
    list_display = [
        'id', 'email', 'name', 'last_login', 'is_staff', 'is_superuser'
    ]
