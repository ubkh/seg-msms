from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm, TransferForm
from lessons.models import User, Transfer


class CreateTransferViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_user.json',
        'lessons/tests/fixtures/alternative_lesson.json',
    ]
    def setUp(self):
        self.form_input = self._create_form_input()
        self.url = reverse('create_transfer')
        self.user = User.objects.get(email='foo@kangaroo.com')
        administrator_group, created = Group.objects.get_or_create(name='Administrator')
        self.user.groups.add(administrator_group)
        self.student = User.objects.get(email='doe@kangaroo.com')
        student_group, created = Group.objects.get_or_create(name='Student')
        self.student.groups.add(student_group)

    def _create_form_input(self):
        form_input = {
            'amount': 100.00,
            'user_id': 2,
            'lesson_id': 3
        }
        return form_input

    def test_create_transfer_url(self):
        self.assertEqual(self.url, '/transfers/create/')

    def get_create_transfer(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfer/record_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TransferForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_transfer(self):
        self.client.login(email=self.user.email, password="Password123")
        self.form_input['user_id'] = 999
        transfer_count_before = Transfer.objects.count()
        response = self.client.post(self.url, self.form_input)
        transfer_count_after = Transfer.objects.count()
        self.assertEqual(transfer_count_before, transfer_count_after)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transfer/record_transfer.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TransferForm))
        self.assertTrue(form.is_bound)

    def test_successful_transfer(self):
        self.client.login(email=self.user.email, password="Password123")
        transfer_count_before = Transfer.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        transfer_count_after = Transfer.objects.count()
        self.assertEqual(transfer_count_before + 1, transfer_count_after)
        response_url = reverse('transfers')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        saved_user = Transfer.objects.latest('id')
        self.assertEqual(saved_user.amount, self.form_input['amount'])
        self.assertEqual(saved_user.user_id, self.form_input['user_id'])
        self.assertEqual(saved_user.lesson_id, self.form_input['lesson_id'])
