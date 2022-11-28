""" Tests for Invoice View"""

from django.test import TestCase
from lessons.models import User, Lesson
from django.urls import reverse
from hashids import Hashids
from django.conf import settings
from lessons.tests.helpers import reverse_with_next

class InvoiceViewTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_user.json', 'lessons/tests/fixtures/default_lesson.json']

    def setUp(self):
        hashids = Hashids(settings.HASHID_SALT, settings.HASHID_LENGTH)
        self.user = User.objects.get(first_name='Foo')
        self.lesson = Lesson.objects.get(title="Test Lesson")
        self.lesson.student = self.user
        self.url = reverse('booking_invoice', args=[self.lesson.id])
        self.lesson.student = self.user

    def test_invoice_accessible_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/invoice.html')


    def test_invoice_not_accessible_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url,follow=True)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_invoice_contains_title(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.title)

    def test_invoice_contains_price(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.price)

    def test_invoice_contains_number_of_lessons(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.number_of_lessons)

    def test_invoice_contains_duration(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.duration)

    def test_invoice_contains_information(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.information)


    def test_invoice_contains_time(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, "1 p.m.")
        
    def test_invoice_contains_interval(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.interval)

    def test_invoice_contains_day(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.day)

    