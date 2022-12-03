from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm, ChildCreateForm, AdminModifyForm
from lessons.models import User, School
from msms.hash import encode


class ModifyAdministratorViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_user.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        self.form_input = self._create_form_input()
        self.school = School.objects.get(id=1)
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.user.set_group_super_administrator()
        # super_administrator_group, created = Group.objects.get_or_create(name='Super-administrator')
        # self.user.groups.add(super_administrator_group)
        self.administrator = User.objects.get(email='doe@kangaroo.com')
        self.administrator.set_group_administrator()
        # administrator_group, created = Group.objects.get_or_create(name='Administrator')
        # self.administrator.groups.add(administrator_group)

    def _create_form_input(self):
        form_input = {
            'first_name': 'Admin',
            'last_name': 'Bar',
            'email': 'admin@kangaroo.com',
            'password': 'Password123',
            'confirm_password': 'Password123'
        }
        return form_input

    def test_modify_administrator_url(self):
        url = reverse('modify_administrator', kwargs={'school': self.school.id, 'pk': self.administrator.pk})
        administrator_id_hash = encode(self.administrator.pk)
        self.assertEqual(url, f'/school/{self.school.id}/administrators/{administrator_id_hash}/modify/')

    def test_get_modify_administrator(self):
        url = reverse('modify_administrator', kwargs={'school': self.school.id, 'pk': self.administrator.pk})
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AdminModifyForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_administrator_modification(self):
        url = reverse('modify_administrator', kwargs={'school': self.school.id, 'pk': self.administrator.pk})
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['email'] = 'kangaroo.com'
        user_count_before = User.objects.count()
        response = self.client.post(url, self.form_input)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/register.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AdminModifyForm))
        self.assertTrue(form.is_bound)

    def test_successful_administrator_modification(self):
        url = reverse('modify_administrator', kwargs={'school': self.school.id, 'pk': self.administrator.pk})
        self.client.login(email=self.user.email, password="Password123")
        user_count_before = User.objects.count()
        response = self.client.post(url, self.form_input, follow=True)
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)
        response_url = reverse('administrators', kwargs={'school': self.school.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'administrators/administrators.html')
        saved_user = User.objects.get(email=self.form_input['email'])
        self.assertEqual(saved_user.first_name, self.form_input['first_name'])
        self.assertEqual(saved_user.last_name, self.form_input['last_name'])
        self.assertTrue(check_password('Password123', saved_user.password))
