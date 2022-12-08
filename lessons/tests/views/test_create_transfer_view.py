from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from lessons.forms import RegisterForm, TransferForm
from lessons.models import User, Transfer, School


class CreateTransferViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_user.json',
        'lessons/tests/fixtures/alternative_lesson.json',
        'lessons/tests/fixtures/default_school.json'
    ]
    def setUp(self):
        self.form_input = self._create_form_input()
        self.school = School.objects.get(id=1)
        self.url = reverse('create_transfer', kwargs={'school': self.school.id})
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.school.set_group_administrator(self.user)
        #self.user.set_group_administrator()
        # administrator_group, created = Group.objects.get_or_create(name='Administrator')
        # self.user.groups.add(administrator_group)
        self.student = User.objects.get(email='doe@kangaroo.com')
        #self.student.set_group_student()
        self.school.set_group_client(self.student)
        # student_group, created = Group.objects.get_or_create(name='Student')
        # self.student.groups.add(student_group)

    def _create_form_input(self):
        form_input = {
            'amount': 100.00,
            'transfer_id': "2-3",
        }
        return form_input

    def test_create_transfer_url(self):
        self.assertEqual(self.url, f'/school/{self.school.id}/transfer/create/')

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
        self.form_input['transfer_id'] = "999-1"
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
        response_url = reverse('school_transfers', kwargs={'school': self.school.id})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        saved_user = Transfer.objects.latest('id')
        self.assertEqual(saved_user.amount, self.form_input['amount'])
        self.assertEqual(saved_user.user_id, 2)
        self.assertEqual(saved_user.lesson_id, 3)
