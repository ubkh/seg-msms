"""
Unit tests of the Request form
"""

import datetime
from django.test import TestCase
from django import forms
from lessons.forms import LessonRequestForm
from lessons.models import Lesson, User


class RequestFormTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.user = User.objects.get(first_name='Foo')
        self.form_input = {
            'student': self.user,
            'title': 'Music Lesson',
            'day': 'Monday',
            'instrument': 'Piano',
            'time': '13:00',
            'number_of_lessons': 2,
            'interval': 1,
            'duration': 60,
            'information': 'New Lesson',
            }

    def test_form_contains_required_fields(self):
        form = LessonRequestForm(user=self.user)
        self.assertIn('title', form.fields)
        self.assertIn('day', form.fields)
        self.assertIn('instrument', form.fields)
        self.assertIn('time', form.fields)
        self.assertIn('number_of_lessons', form.fields)
        self.assertIn('interval', form.fields)
        self.assertIn('duration', form.fields)
        self.assertIn('information', form.fields)
        time_field = form.fields['time']
        self.assertTrue(isinstance(time_field, forms.TimeField))
        day_field = form.fields['day']
        self.assertTrue(isinstance(day_field, forms.ChoiceField))
        instrument_field = form.fields['instrument']
        self.assertTrue(isinstance(instrument_field, forms.ChoiceField))

    def test_form_saves_correctly(self):
        form = LessonRequestForm(data=self.form_input, user=self.user)
        lesson_count_before = Lesson.objects.count()
        lesson = form.save(commit=False)
        lesson.student = self.user
        lesson.save()
        lesson_count_after = Lesson.objects.count()
        self.assertEqual(lesson_count_before + 1, lesson_count_after)
        saved_lesson = Lesson.objects.get(title=self.form_input['title'])
        self.assertEqual(saved_lesson.title, self.form_input['title'])
        self.assertEqual(saved_lesson.day, self.form_input['day'])
        self.assertEqual(saved_lesson.instrument, self.form_input['instrument'])
        self.assertEqual(saved_lesson.time, datetime.time(13,0))
        self.assertEqual(saved_lesson.number_of_lessons, self.form_input['number_of_lessons'])
        self.assertEqual(saved_lesson.interval, self.form_input['interval'])
        self.assertEqual(saved_lesson.duration, self.form_input['duration'])
        self.assertEqual(saved_lesson.information, self.form_input['information'])

    def test_form_uses_number_of_lessons_validation(self):
        self.form_input['number_of_lessons'] = -1
        form = LessonRequestForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_uses_day_validation(self):
        self.form_input['day'] = 'Wrong_Day'
        form = LessonRequestForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_uses_instrument_validation(self):
        self.form_input['instrument'] = 'Wrong_Instrument'
        form = LessonRequestForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_uses_interval_validation(self):
        self.form_input['interval'] = -1
        form = LessonRequestForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())

    def test_form_uses_duration_validation(self):
        self.form_input['duration'] = -1.5
        form = LessonRequestForm(data=self.form_input, user=self.user)
        self.assertFalse(form.is_valid())