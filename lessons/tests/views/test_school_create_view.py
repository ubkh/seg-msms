from unittest import skip

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm, SchoolCreateForm
from lessons.models import User, School


class SchoolCreateViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.url = reverse('create_school')
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.user.set_group_director()
        self.form_input = self._create_form_input()


    def _create_form_input(self):
        form_input = {
            'name': 'New School',
            'description': 'Test',
        }
        return form_input

    def test_create_school_url(self):
        school_create_url = f"/school/create/"
        self.assertEqual(self.url, school_create_url)

    def test_get_school_create(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/create_school.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SchoolCreateForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_registration(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['name'] = ''
        school_count_before = School.objects.count()
        response = self.client.post(self.url, self.form_input)
        school_count_after = School.objects.count()
        self.assertEqual(school_count_before, school_count_after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/create_school.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SchoolCreateForm))
        self.assertTrue(form.is_bound)

    def test_successful_registration(self):
        self.client.login(email=self.user.email, password="Password123")
        school_count_before = School.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        school_count_after = School.objects.count()
        self.assertEqual(school_count_before + 1, school_count_after)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')
        saved_school = School.objects.get(name='New School')
        self.assertEqual(saved_school.name, self.form_input['name'])
        self.assertEqual(saved_school.description, self.form_input['description'])
