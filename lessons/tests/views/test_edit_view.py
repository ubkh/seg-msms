"""
Tests that will be used to test the Edit view.
"""

from django.test import TestCase
from django.urls import reverse
from lessons.models import User
from lessons.forms import EditUserForm


class EditViewTestCase(TestCase):
    """
    Unit tests that will be used to test the Edit view.
    """

    def setUp(self):
        self.form_input = self._create_form_input()
        self.url = reverse('edit_profile')
        self.user = User.objects.get(email='doe@kangaroo.com')

    def _create_form_input(self):
        form_input = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'email': 'foo@kangaroo.com',
        }
        return form_input

    def test_edit_url(self):
        self.assertEqual(self.url, '/edit_profile/')

    def test_get_edit(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/edit_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditUserForm))
        self.assertFalse(form.is_bound)
