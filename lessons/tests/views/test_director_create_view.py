from unittest import skip

from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm
from lessons.models import User, School


class DirectorCreateViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.url = reverse('create_director')
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.user.set_group_system_administrator()
        self.form_input = self._create_form_input()

    def _create_form_input(self):
        form_input = {
            'first_name': 'Admin',
            'last_name': 'Bar',
            'email': 'admin@kangaroo.com',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }
        return form_input

    def test_create_director_url(self):
        director_url = f"/director/create/"
        self.assertEqual(self.url, director_url)

    def test_get_create_director(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/create_director.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_registration(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['email'] = 'kangaroo.com'
        user_count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/create_director.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RegisterForm))
        self.assertTrue(form.is_bound)

    def test_successful_registration(self):
        self.client.login(email=self.user.email, password="Password123")
        user_count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'school/list_school.html')
        saved_director = User.objects.get(email=self.form_input['email'])
        self.assertEqual(saved_director.first_name, self.form_input['first_name'])
        self.assertEqual(saved_director.last_name, self.form_input['last_name'])
        self.assertTrue(saved_director.groups.filter(name='Director').exists())
        self.assertTrue(check_password('Password123', saved_director.password))
