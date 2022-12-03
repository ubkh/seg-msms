"""
Tests of the index view
"""

from django.test import TestCase
from django.urls import reverse
from lessons.models import User

class IndexViewTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.url = reverse('index')
        self.user = User.objects.get(email='foo@kangaroo.com')
    
    def test_index_url(self):
        self.assertEqual(self.url, '/')
    
    def test_get_index(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_get_index_with_redirect_when_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')