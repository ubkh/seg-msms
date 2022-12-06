"""
Tests that will be used to test the Registration form.
"""

from django import forms
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from lessons.models import User
from lessons.forms import TeacherRegisterForm
from multiselectfield import MultiSelectField


class TeacherRegisterFormTestCase(TestCase):
    """
    Unit tests that will be used to test the Registration form.
    """

    def setUp(self):
        self.form_input = self._create_form_input()

    def _create_form_input(self):
        form_input = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@kangaroo.com',
            'password': 'Example123',
            'instrument': ['Piano'],
            'confirm_password': 'Example123',
            'make_account_adult_student': 'False'
        }
        return form_input

    def test_teacher_register_form_is_valid(self):
        teacher_register_form = TeacherRegisterForm(data=self.form_input)
        self.assertTrue(teacher_register_form.is_valid())

    def tests_form_saves_correctly(self):
        teacher_register_form = TeacherRegisterForm(data=self.form_input)
        user_count_before = User.objects.count()
        teacher_register_form.save()
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)
        saved_user = User.objects.get(email=self.form_input['email'])
        self.assertEqual(saved_user.first_name, self.form_input['first_name'])
        self.assertEqual(saved_user.last_name, self.form_input['last_name'])
        self.assertEqual(saved_user.instrument, self.form_input['instrument'])
        self.assertTrue(check_password(self.form_input['password'], saved_user.password))

    def test_form_uses_model_email_validation(self):
        self.form_input['email'] = 'kangaroo.com'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_model_first_name_validation(self):
        self.form_input['first_name'] = 'n@me'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_model_last_name_validation(self):
        self.form_input['last_name'] = 'n@me'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_uses_model_instrument_validation(self):
        self.form_input['instrument'] = 't@co'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['password'] = 'EXAMPLE123'
        self.form_input['confirm_password'] = 'EXAMPLE123'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_upper_character(self):
        self.form_input['password'] = 'example123'
        self.form_input['confirm_password'] = 'example123'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_a_digit(self):
        self.form_input['password'] = 'Example'
        self.form_input['confirm_password'] = 'Example'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_can_contain_six_characters(self):
        self.form_input['password'] = 'Examp1'
        self.form_input['confirm_password'] = 'Examp1'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_password_can_contain_seven_or_more_characters(self):
        self.form_input['password'] = 'Examp12'
        self.form_input['confirm_password'] = 'Examp12'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_password_cannot_contain_five_or_less_characters(self):
        self.form_input['password'] = 'Exam1'
        self.form_input['confirm_password'] = 'Exam1'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_and_password_confirmation_are_the_same(self):
        self.form_input['password'] = 'Password123'
        self.form_input['confirm_password'] = 'PAssword1234'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_make_account_adult_student_can_be_true(self):
        self.form_input['make_account_adult_student'] = 'True'
        form = TeacherRegisterForm(data=self.form_input)
        self.assertTrue(form.is_valid())
