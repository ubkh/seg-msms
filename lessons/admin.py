"""
Configuration of the admin interface for the music school management system.
Register your models here.
"""

from dataclasses import field
from django.contrib import admin
from .models import User, Lesson, Transfer, Term


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Configuration of the admin interface to display users.
    """
    list_display = [
        'id', 'email', 'first_name', 'last_name', 'last_login', 'is_staff', 'is_superuser'
    ]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Configuration of the admin interface to display lessons.
    """
    list_display = [
        'id', 'fulfilled', 'student', 'day', 'time', 'number_of_lessons', 'interval', 'duration', 'title',
        'information', 'price'
    ]


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    """
    Configuration of the admin interface to display transfers.
    """
    list_display = [
        'id', 'user', 'lesson', 'amount'
    ]

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    """
    Configuration of the admin interface to display terms.
    """
    list_display = [
        f.name for f in Term._meta.fields
    ]