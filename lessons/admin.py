"""
Configuration of the admin interface for the music school management system.
"""

from django.contrib import admin
from .models import User, Lesson

# Register your models here.
admin.site.register(Lesson)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface to display users."""
    list_display = [
        'id', 'email', 'name', 'last_login', 'is_staff', 'is_superuser'
    ]
