from unittest import skip

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm
from lessons.models import User, School, Lesson


class BookingListViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json',
        'lessons/tests/fixtures/other_user.json',
    ]

    def setUp(self):
        self.school = School.objects.get(id=1)
        self.url = reverse('school_bookings', kwargs={'school': self.school.id})
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.school.set_group_administrator(self.user)
        self.other_user = User.objects.get(email='doe@kangaroo.com')

    def test_display_booking_list_url(self):
        self.assertEqual(self.url, f'/school/{self.school.id}/bookings/')

    def test_get_lessons_list(self):
        self.client.login(email=self.user.email, password="Password123")
        first_lesson = Lesson(school=self.school, student=self.other_user, teacher=self.user, title="Lesson One")
        first_lesson.save()
        second_lesson = Lesson(school=self.school, student=self.other_user, teacher=self.user, title="Lesson Tow")
        second_lesson.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lessons/bookings.html')
        self.assertEqual(len(response.context['lessons']), 2)
        self.assertContains(response, first_lesson.title)
        self.assertContains(response, second_lesson.title)

