"""
Unit tests of the login form
"""

from django.test import TestCase
from django import forms
from lessons.forms import LoginForm

class LoginFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {'name': 'Foo', 'email': 'fookangaroo@example.com', 'password': 'Password123'}
    
    def test_form_contains_required_fields(self):
        form = LoginForm()
        self.assertIn('name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
    
    def test_form_accepts_valid_input(self):
        form = LoginForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_blank_nMW(self):
        self.form_input['name'] = ''
        form = LoginForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_email(self):
        self.form_input['email'] = ''
        form = LoginForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LoginForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_accepts_incorrect_name(self):
        self.form_input['name'] = 'lm'
        form = LoginForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_incorrect_email(self):
        self.form_input['email'] = 'fookangaroo'
        form = LoginForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'ao'
        form = LoginForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    

