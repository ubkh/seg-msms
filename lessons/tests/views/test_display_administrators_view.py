from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm
from lessons.models import User


class DisplayAdministratorViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_user.json'
    ]

    def setUp(self):
        self.url = reverse('administrators')
        self.user = User.objects.get(email='foo@kangaroo.com')
        super_administrator_group, created = Group.objects.get_or_create(name='Super-administrator')
        self.user.groups.add(super_administrator_group)
        self.administrator = User.objects.get(email='doe@kangaroo.com')
        administrator_group, created = Group.objects.get_or_create(name='Administrator')
        self.administrator.groups.add(administrator_group)

    def test_display_administrator_url(self):
        self.assertEqual(self.url, '/administrators/')

    def test_get_administrators(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'administrators/administrators.html')
        self.assertEqual(len(response.context['administrators']), 1)
        self.assertContains(response, self.administrator.email)
        self.assertContains(response, self.administrator.first_name)
        self.assertContains(response, self.administrator.last_name)
        user = User.objects.get(email=self.administrator.email)
        modify_administrator_url = reverse('modify_administrator', kwargs={'pk': user.pk})
        self.assertContains(response, modify_administrator_url)

