"""
Tests that will be used to test the Edit view.
"""
from django.contrib.auth import login
from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.forms import EditUserForm
from msms.hash import hashids, encode


class EditViewTestCase(TestCase):
    """
    Unit tests that will be used to test the Edit view.
    """

    fixtures = [
        'lessons/tests/fixtures/other_user.json'
    ]


    def setUp(self):
        self.form_input = self._create_form_input()
        self.user = User.objects.get(email='doe@kangaroo.com')
        self.url = reverse('edit_profile', kwargs={'pk': self.user.id})

    def _create_form_input(self):
        form_input = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@kangaroo.com',
        }
        return form_input

    def test_edit_url(self):
        self.assertEqual(self.url, f'/profile/{encode(self.user.id)}/edit/')

    def test_get_edit(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditUserForm))
        self.assertFalse(form.is_bound)
