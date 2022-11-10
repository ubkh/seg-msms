"""Unit tests of the login form"""

from django.test import TestCase
from django import forms
from lessons.forms import LoginForm

class LoginFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {'username': '@foo', 'password': 'Password123'}
    
    def test_form_contains_required_fields(self):
        form = LoginForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
    
    def test_form_accepts_valid_input(self):
        form = LoginForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = LoginForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = LoginForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'lm'
        form = LoginForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'ao'
        form = LoginForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    

