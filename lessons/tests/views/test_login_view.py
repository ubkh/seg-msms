"""
Tests of the login view
"""

from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from lessons.forms import LoginForm
from lessons.models import User
from lessons.tests.helpers import LoginTester, reverse_with_next
from django.contrib import messages

class LoginViewTestCase(TestCase, LoginTester):
    fixtures = ['lessons/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(email='foo@kangaroo.com')
    
    def test_login_url(self):
        self.assertEqual(self.url, '/log_in/')
    
    def test_get_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LoginForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(next)
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 0)
    
    def test_get_login_with_redirect(self):
        destination_url = reverse('home')
        self.url = reverse_with_next('log_in', destination_url)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        form = response.context['form']
        next = response.context['next']
        self.assertTrue(isinstance(form, LoginForm))
        self.assertFalse(form.is_bound)
        self.assertEqual(next, destination_url)
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 0)
    
    def test_get_login_with_redirect_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')

    def test_unsuccessful_login(self):
        form_input = {'name': 'Foo Bar', 'email': 'fookangaroo.com', 'password': 'wrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LoginForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 1)
        self.assertEqual(message_list[0].level, messages.ERROR)
    
    def test_login_successful(self):
        form_input = {'name': 'Foo Bar', 'email': 'foo@kangaroo.com', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 0)
    
    def test_login_successful_with_redirect(self):
        redirect_url = reverse('home')
        form_input = {'name': 'Foo Bar', 'email': 'foo@kangaroo.com', 'password': 'Password123', 'next': redirect_url}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')
        message_list = list(response.context['messages'])
        self.assertEqual(len(message_list), 0)
    
    def test_post_login_redirect_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        form_input = {'email': 'foobar@kangaroo.com', 'Password': 'wrongPassword123'}
        response = self.client.post(self.url, form_input, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')

