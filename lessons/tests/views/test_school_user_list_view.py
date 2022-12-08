from unittest import skip

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm
from lessons.models import User, School


class SchoolUserListViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_user.json',
        'lessons/tests/fixtures/default_school.json',
    ]

    def setUp(self):
        self.school = School.objects.get(id=1)
        self.url = reverse('members', kwargs={'school': self.school.id})
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.school.set_group_super_administrator(self.user)
        self.student = User.objects.get(email='doe@kangaroo.com')
        self.school.set_group_client(self.student)

    def test_school_user_list_url(self):
        self.assertEqual(self.url, f'/school/{self.school.id}/members/')

    def test_get_user_list(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/users.html')
        self.assertEqual(len(response.context['school_admissions']), 2)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.student.first_name)
        self.assertContains(response, self.student.last_name)
        self.assertContains(response, self.student.email)
