"""
Unit tests of the Request form
"""

import datetime


from django.forms import TypedChoiceField
from django.test import TestCase
from django import forms
from django.utils.regex_helper import Choice

from lessons.forms import LessonModifyForm
from lessons.models import Lesson, User, School


class LessonModifyFormTestCase(TestCase):
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
        teacher_user = User.objects.create_user(
            email="sylvia.plath@example.org",
            first_name="Albert",
            last_name="Camus",
            instrument=["Piano", "Violin"],
            password="Password123",
        )
        teacher_user.set_group_user()
        self.school.set_group_teacher(teacher_user)
        self.form_input = {
            'student': self.user,
            'title': 'Music Lesson',
            'day': 'Monday',
            'instrument': 'Piano',
            'teacher': teacher_user,
            'time': '13:00',
            'interval': 1,
            'duration': 60,
            'number_of_lessons': 1,
            'information': 'New Lesson',
        }

    def test_form_contains_required_fields(self):
        form = LessonModifyForm(user=self.user, school=self.school)
        self.assertIn('title', form.fields)
        self.assertIn('day', form.fields)
        self.assertIn('instrument', form.fields)
        self.assertIn('time', form.fields)
        self.assertIn('interval', form.fields)
        self.assertIn('duration', form.fields)
        self.assertIn('information', form.fields)
        time_field = form.fields['time']
        self.assertTrue(isinstance(time_field, forms.TimeField))
        day_field = form.fields['day']
        self.assertTrue(isinstance(day_field, forms.ChoiceField))
        instrument_field = form.fields['instrument']
        self.assertTrue(isinstance(instrument_field, forms.ChoiceField))
        teacher_field = form.fields['teacher']
        self.assertTrue(isinstance(teacher_field, forms.ChoiceField))

    def test_form_saves_correctly(self):
        form = LessonModifyForm(data=self.form_input, user=self.user, school=self.school)
        lesson_count_before = Lesson.objects.count()
        lesson = form.save(commit=False)
        lesson.student = self.user
        lesson.school = self.school
        lesson.save()
        lesson_count_after = Lesson.objects.count()
        self.assertEqual(lesson_count_before + 1, lesson_count_after)
        saved_lesson = Lesson.objects.get(title=self.form_input['title'])
        self.assertEqual(saved_lesson.title, self.form_input['title'])
        self.assertEqual(saved_lesson.day, self.form_input['day'])
        self.assertEqual(saved_lesson.instrument, self.form_input['instrument'])
        self.assertEqual(saved_lesson.teacher, self.form_input['teacher'])
        self.assertEqual(saved_lesson.time, datetime.time(13,0))
        self.assertEqual(saved_lesson.interval, self.form_input['interval'])
        self.assertEqual(saved_lesson.duration, self.form_input['duration'])
        self.assertEqual(saved_lesson.information, self.form_input['information'])

    def test_form_uses_day_validation(self):
        self.form_input['day'] = 'Wrong_Day'
        form = LessonModifyForm(data=self.form_input, user=self.user, school=self.school)
        self.assertFalse(form.is_valid())

    def test_form_uses_instrument_validation(self):
        self.form_input['instrument'] = 'Wrong_Instrument'
        form = LessonModifyForm(data=self.form_input, user=self.user, school=self.school)
        self.assertFalse(form.is_valid())

    def test_form_uses_teacher_validation(self):
        self.form_input['teacher'] = 'Wrong_teacher'
        form = LessonModifyForm(data=self.form_input, user=self.user, school=self.school)
        self.assertFalse(form.is_valid())

    def test_form_uses_interval_validation(self):
        self.form_input['interval'] = -1
        form = LessonModifyForm(data=self.form_input, user=self.user, school=self.school)
        self.assertFalse(form.is_valid())

    def test_form_uses_duration_validation(self):
        self.form_input['duration'] = -1.5
        form = LessonModifyForm(data=self.form_input, user=self.user, school=self.school)
        self.assertFalse(form.is_valid())
