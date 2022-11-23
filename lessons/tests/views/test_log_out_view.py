"""
Tests of the log out view
"""

from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.tests.helpers import LoginTester

class LogOutViewTestCase(TestCase, LoginTester):
    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(first_name='Foo')
    
    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')
    
    def test_get_log_out(self):
        self.client.login(name='Foo Bar', email='foo@kangaroo.com', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('index')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertFalse(self._is_logged_in())

