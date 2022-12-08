"""
Unit tests of the Request form
"""

import datetime
from unittest import skip

from django.forms import TypedChoiceField
from django.test import TestCase
from django import forms
from django.utils.regex_helper import Choice

from lessons.forms import LessonFulfillForm
from lessons.models import Lesson, User, School


class LessonFulfillFormTestCase(TestCase):
    """
    Unit tests that will be used to test the Registration form.
    """
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        self.user = User.objects.get(first_name='Foo')
        self.school = School.objects.get(id=1)
        self.form_input = {
            'student': self.user,
            'school': self.school.id,
            'title': 'Music Lesson',
            'day': 'Monday',
            'time': '13:00',
            'interval': 1,
            'duration': 60,
            'number_of_lessons': 1,
            'information': 'New Lesson',
        }

    def test_form_contains_required_fields(self):
        form = LessonFulfillForm(data=self.form_input, initial=self.form_input)
        self.assertIn('day', form.fields)
        self.assertIn('time', form.fields)
        self.assertIn('interval', form.fields)
        self.assertIn('duration', form.fields)
        time_field = form.fields['time']
        self.assertTrue(isinstance(time_field, forms.TimeField))
        day_field = form.fields['day']
        self.assertTrue(isinstance(day_field, forms.ChoiceField))

    def test_form_saves_correctly(self):
        form = LessonFulfillForm(data=self.form_input, initial=self.form_input)
        lesson_count_before = Lesson.objects.count()
        lesson = form.save(commit=False)
        lesson.student = self.user
        lesson.school = self.school
        teacher = User(email="teacher@example.org")
        teacher.save()
        lesson.teacher = teacher
        lesson.save()
        lesson_count_after = Lesson.objects.count()
        self.assertEqual(lesson_count_before + 1, lesson_count_after)
        saved_lesson = Lesson.objects.get(title=self.form_input['title'])
        self.assertEqual(saved_lesson.title, self.form_input['title'])
        self.assertEqual(saved_lesson.day, self.form_input['day'])
        self.assertEqual(saved_lesson.time, datetime.time(13, 0))
        self.assertEqual(saved_lesson.interval, self.form_input['interval'])
        self.assertEqual(saved_lesson.duration, self.form_input['duration'])

    def test_form_uses_day_validation(self):
        self.form_input['day'] = 'Wrong_Day'
        form = LessonFulfillForm(data=self.form_input, initial=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_interval_validation(self):
        self.form_input['interval'] = -1
        form = LessonFulfillForm(data=self.form_input, initial=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_duration_validation(self):
        self.form_input['duration'] = -1.5
        form = LessonFulfillForm(data=self.form_input, initial=self.form_input)
        self.assertFalse(form.is_valid())
