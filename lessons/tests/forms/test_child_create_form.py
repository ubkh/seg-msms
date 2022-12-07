"""
Tests that will be used to test the Child Create form.
"""

from django.test import TestCase
from django import forms

from lessons.forms import ChildCreateForm
from lessons.models import User


class ChildCreateFormTestCase(TestCase):
    """
    Unit tests that will be used to test the Child Create form.
    """

    def setUp(self):
        self.form_input = self._create_form_input()

    def _create_form_input(self):
        form_input = {
            'first_name': 'Foo',
            'last_name': 'Bar',
        }
        return form_input

    def test_child_create_form_is_valid(self):
        register_form = ChildCreateForm(data=self.form_input)
        self.assertTrue(register_form.is_valid())

    def test_child_create_form_contains_required_fields(self):
        child_create_form = ChildCreateForm()
        self.assertIn('first_name', child_create_form.fields)
        first_name_field = child_create_form.fields['first_name']
        self.assertTrue(isinstance(first_name_field, forms.CharField))
        self.assertIn('last_name', child_create_form.fields)
        last_name_field = child_create_form.fields['last_name']
        self.assertTrue(isinstance(last_name_field, forms.CharField))

    def test_form_saves_correctly(self):
        child_create_form = ChildCreateForm(data=self.form_input)
        user_count_before = User.objects.count()
        child_create_form.save()
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)
        saved_user = User.objects.latest('id')
        self.assertEqual(saved_user.first_name, self.form_input['first_name'])
        self.assertEqual(saved_user.last_name, self.form_input['last_name'])

    def test_form_uses_model_first_name_validation(self):
        self.form_input['first_name'] = 'n@me'
        form = ChildCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_model_last_name_validation(self):
        self.form_input['last_name'] = 'n@me'
        form = ChildCreateForm(data=self.form_input)
        self.assertFalse(form.is_valid())
