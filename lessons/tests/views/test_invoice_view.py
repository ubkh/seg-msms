""" Tests for Invoice View"""

from django.test import TestCase
from lessons.models import User, Lesson, School
from django.urls import reverse
from lessons.tests.helpers import reverse_with_next

class InvoiceViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_lesson.json',
        'lessons/tests/fixtures/other_lesson.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        self.user = User.objects.get(first_name='Foo')
        self.lesson = Lesson.objects.get(title="Test Lesson")
        self.lesson.student = self.user
        self.school = School.objects.get(id=1)
        self.school.set_group_client(self.user)
        self.url = reverse('booking_invoice', kwargs={'school': self.school.id, 'pk': self.lesson.id})
        self.lesson.student = self.user
        self.other_lesson = Lesson.objects.get(title="Test Lesson 2")

    def test_invoice_accessible_logged_in(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/invoice.html')


    def test_invoice_not_accessible_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
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

    def test_invoice_contains_instrument(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.instrument)
    
    def test_invoice_contains_teacher(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertContains(response, self.lesson.teacher)

    def test_invoice_not_accessible_when_not_fulfilled(self):
        other_url = reverse('booking_invoice', kwargs={'school': self.school.id, 'pk': self.other_lesson.id})
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(other_url, follow=True)
        redirect_url = reverse('home')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')
