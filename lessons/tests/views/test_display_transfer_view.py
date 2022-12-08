from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm
from lessons.models import User, Transfer, School


class DisplayTransferViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json',
        'lessons/tests/fixtures/other_user.json',
        'lessons/tests/fixtures/alternative_lesson.json',
        'lessons/tests/fixtures/default_transfer.json',
    ]

    def setUp(self):
        self.school = School.objects.get(id=1)
        self.url = reverse('school_transfers', kwargs={'school': self.school.id})
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.school.set_group_administrator(self.user)
        self.transfer = Transfer.objects.get(id='1')

    def test_display_administrator_url(self):
        self.assertEqual(self.url, f'/school/{self.school.id}/transfers/')

    def test_get_transfers(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfer/transfers.html')
        self.assertEqual(len(response.context['transfers']), 1)
        self.assertContains(response, self.transfer.amount)
        self.assertContains(response, self.transfer.user_id)
        self.assertContains(response, self.transfer.lesson_id)