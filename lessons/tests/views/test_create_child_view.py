from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm, ChildCreateForm
from lessons.models import User


class CreateChildViewTestCase(TestCase):
    fixtures = ['lessons/tests/fixtures/default_user.json']

    def setUp(self):
        self.form_input = self._create_form_input()
        self.url = reverse('create_child')
        self.user = User.objects.get(email='foo@kangaroo.com')
        adult_student_group, created = Group.objects.get_or_create(name='Adult-user')
        self.user.groups.add(adult_student_group)

    def _create_form_input(self):
        form_input = {
            'first_name': 'Baz',
            'last_name': 'Daz',
        }
        return form_input

    def test_create_child_url(self):
        self.assertEqual(self.url, '/children/create/')

    def test_get_create_child(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/create_child.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ChildCreateForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_child_creation(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['first_name'] = ''
        user_count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'children/create_child.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ChildCreateForm))
        self.assertTrue(form.is_bound)

    def test_successful_child_creation(self):
        self.client.login(email=self.user.email, password="Password123")
        user_count_before = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before + 1, user_count_after)
        response_url = reverse('children')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'children/children.html')
        saved_user = User.objects.latest('id')
        self.assertEqual(saved_user.first_name, self.form_input['first_name'])
        self.assertEqual(saved_user.last_name, self.form_input['last_name'])
