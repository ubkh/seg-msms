"""
Configuration of the admin interface for the music school management system.
Register your models here.
"""

from dataclasses import field
from django.contrib import admin
from django.contrib.admin import display

from lessons.models.lesson import ScheduledLesson

from .models import User, Lesson, Transfer, Term, School, Admission


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
        'id', 'fulfilled', 'student', 'day', 'time', 'interval', 'duration', 'title',
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


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'director', 'current_term'
    ]


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'school', 'client', 'is_active'
    ]


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    """
    Configuration of the admin interface to display terms.
    """
    list_display = [
        f.name for f in Term._meta.fields
    ]

@admin.register(ScheduledLesson)
class ScheduledLessonAdmin(admin.ModelAdmin):
    """
    Configuration of the admin interface to display scheduled lessons.
    """
    list_display = [
        f.name for f in ScheduledLesson._meta.fields
    ]