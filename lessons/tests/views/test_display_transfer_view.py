from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm
from lessons.models import User, Transfer


class DisplayTransferViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_user.json',
        'lessons/tests/fixtures/alternative_lesson.json',
        'lessons/tests/fixtures/default_transfer.json'
    ]

    def setUp(self):
        self.url = reverse('transfers')
        self.user = User.objects.get(email='foo@kangaroo.com')
        administrator_group, created = Group.objects.get_or_create(name='Administrator')
        self.user.groups.add(administrator_group)
        self.transfer = Transfer.objects.get(id='1')

    def test_display_administrator_url(self):
        self.assertEqual(self.url, '/transfers/')

    def test_get_transfers(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfer/transfers.html')
        self.assertEqual(len(response.context['transfers']), 1)
        self.assertContains(response, self.transfer.amount)
        self.assertContains(response, self.transfer.user_id)
        self.assertContains(response, self.transfer.lesson_id)