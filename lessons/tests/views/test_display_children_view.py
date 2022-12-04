from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm
from lessons.models import User


class DisplayChildrenViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_child.json'
    ]

    def setUp(self):
        self.url = reverse('children')
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.user.set_group_adult_user()
        # adult_student_group, created = Group.objects.get_or_create(name='Adult-student')
        # self.user.groups.add(adult_student_group)
        self.child = User.objects.get(id='3')

    def test_children_url(self):
        self.assertEqual(self.url, '/children/')

    def test_get_children(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/children.html')
        self.assertEqual(len(response.context['children']), 1)
        self.assertContains(response, self.child.first_name)
        self.assertContains(response, self.child.last_name)