"""
Tests that will be used to test the Registration view.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password
from lessons.models import User
from lessons.forms import RegisterForm
from lessons.tests.helpers import LoginTester


class RegisterViewTestCase(TestCase, LoginTester):
    """
    Unit tests that will be used to test the Registration view.
    """
    fixtures = ['lessons/tests/fixtures/other_user.json']

    def setUp(self):
        self.form_input = self._create_form_input()
        self.url = reverse('register')
        self.user = User.objects.get(email='doe@kangaroo.com')

    def _create_form_input(self):
        form_input = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@kangaroo.com',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }
        return form_input

    def test_register_url(self):
        self.assertEqual(self.url, '/register/')

    def test_get_register(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertFalse(form.is_bound)

    def test_get_register_with_redirect_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')

    def test_unsuccessful_registration(self):
        self.form_input['email'] = 'kangaroo.com'
        user_count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_registration(self):
        user_count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')
        saved_user = User.objects.get(email=self.form_input['email'])
        self.assertEqual(saved_user.first_name, self.form_input['first_name'])
        self.assertEqual(saved_user.last_name, self.form_input['last_name'])
        self.assertTrue(check_password('Password123', saved_user.password))
        self.assertTrue(self._is_logged_in())

    def test_post_register_redirect_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        user_count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')
