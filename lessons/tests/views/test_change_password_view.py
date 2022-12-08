from django.test import TestCase

from django.urls import reverse

from lessons.models import User, School
from msms.hash import encode


class ChangePasswordViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.url = reverse('password_change', kwargs={'pk': self.user.id})
        self.form_input = {
            'old_password': 'Password123',
            'new_password': 'Test123',
            'confirm_password': 'Test123'
        }

    def test_change_password_url(self):
        self.assertEqual(self.url, f'/profile/{encode(self.user.id)}/password_change/')

    def test_get_change_password(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/change_password.html')
        form = response.context['form']
        self.assertFalse(form.is_bound)
