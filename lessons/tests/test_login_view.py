"""
Tests of the login view
"""

from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import LoginForm
from lessons.models import User
from .helpers import LoginTester
from django.contrib import messages

class LoginViewTestCase(TestCase, LoginTester):
    def setUp(self):
        self.url = reverse('login')
        User.objects.create_user(
            email='kangaroo@example.com',
            name='Foo',
            password='Password123',
        )
    
    def test_login_url(self):
        self.assertEqual(self.url, '/login/')
    
    def test_get_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginForm))
        self.assertFalse(form.is_bound)
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 0)

    def test_unsuccessful_login(self):
        form_input = { 'name': 'Foo', 'email': 'fookangaroo@example.com', 'password': 'wrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 1)
        self.assertEqual(message_list[0].level, messages.ERROR)
    
    def test_login_successful(self):
        form_input = { 'name': 'Foo', 'email': 'kangaroo@example.com', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 0)

