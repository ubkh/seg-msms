"""
Tests that will be used to test the Edit User form.
"""

from django import forms
from django.test import TestCase
from django.contrib.auth.hashers import check_password
from lessons.models import User
from lessons.forms import EditUserForm


class EditFormTestCase(TestCase):
    """
    Unit tests that will be used to test the Edit User form.
    """

    def setUp(self):
        self.form_input = self._create_form_input()

    def _create_form_input(self):
        form_input = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@kangaroo.com',
        }
        return form_input

    def test_edit_form_is_valid(self):
        register_form = EditUserForm(data=self.form_input)
        self.assertTrue(register_form.is_valid())

    def test_edit_form_contains_required_fields(self):
        register_form = EditUserForm()
        self.assertIn('first_name', register_form.fields)
        first_name_field = register_form.fields['first_name']
        self.assertTrue(isinstance(first_name_field, forms.CharField))
        self.assertIn('last_name', register_form.fields)
        last_name_field = register_form.fields['last_name']
        self.assertTrue(isinstance(last_name_field, forms.CharField))
        self.assertIn('email', register_form.fields)
        email_field = register_form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))

    def tests_form_saves_correctly(self):
        register_form = EditUserForm(data=self.form_input)
        user_count_before = User.objects.count()
        register_form.save()
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)
        saved_user = User.objects.get(email=self.form_input['email'])
        self.assertEqual(saved_user.first_name, self.form_input['first_name'])
        self.assertEqual(saved_user.last_name, self.form_input['last_name'])

    def test_form_uses_model_email_validation(self):
        self.form_input['email'] = 'kangaroo.com'
        form = EditUserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_model_first_name_validation(self):
        self.form_input['first_name'] = 'n@me'
        form = EditUserForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_model_last_name_validation(self):
        self.form_input['last_name'] = 'n@me'
        form = EditUserForm(data=self.form_input)
        self.assertFalse(form.is_valid())