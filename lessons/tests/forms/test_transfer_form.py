from decimal import Decimal

from django.test import TestCase
from django import forms

from lessons.forms import TransferForm
from lessons.models import Transfer


class TransferFormTestCase(TestCase):
    """
    Unit tests that will be used to test the Registration form.
    """

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_lesson.json',
        'lessons/tests/fixtures/other_user.json',
        'lessons/tests/fixtures/other_lesson.json',
        'lessons/tests/fixtures/alternative_lesson.json'
    ]

    def setUp(self):
        self.form_input = self._create_form_input()

    def _create_form_input(self):
        form_input = {
            'amount': 100.00,
            'user_id': 1,
            'lesson_id': 1
        }
        return form_input

    def test_transfer_form_is_valid(self):
        register_form = TransferForm(data=self.form_input)
        self.assertTrue(register_form.is_valid())

    def test_transfer_from_contains_required_fields(self):
        transfer_form = TransferForm()
        self.assertIn('amount', transfer_form.fields)
        amount_field = transfer_form.fields['amount']
        self.assertTrue(isinstance(amount_field, forms.DecimalField))
        self.assertIn('user_id', transfer_form.fields)
        user_id_field = transfer_form.fields['user_id']
        self.assertTrue(isinstance(user_id_field, forms.IntegerField))
        self.assertIn('lesson_id', transfer_form.fields)
        lesson_id_field = transfer_form.fields['lesson_id']
        self.assertTrue(isinstance(lesson_id_field, forms.IntegerField))

    def test_form_saves_correctly(self):
        transfer_form = TransferForm(data=self.form_input)
        transfer_count_before = Transfer.objects.count()
        transfer_form.save()
        transfer_count_after = Transfer.objects.count()
        self.assertEqual(transfer_count_before + 1, transfer_count_after)
        saved_transfer = Transfer.objects.latest('id')
        self.assertEqual(saved_transfer.amount, self.form_input['amount'])
        self.assertEqual(saved_transfer.user_id, self.form_input['user_id'])
        self.assertEqual(saved_transfer.lesson_id, self.form_input['lesson_id'])

    def test_form_uses_model_amount_validation(self):
        self.form_input['amount'] = -1.001
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_student_can_make_multiple_transfers_for_different_lessons(self):
        transfer_form = TransferForm(data=self.form_input)
        transfer_count_before = Transfer.objects.count()
        transfer_form.save()
        second_form_input = {
            'amount': 100.00,
            'user_id': 1,
            'lesson_id': 2
        }
        second_transfer_form = TransferForm(data=second_form_input)
        second_transfer_form.save()
        transfer_count_after = Transfer.objects.count()
        self.assertEqual(transfer_count_before + 2, transfer_count_after)
        saved_second_transfer = Transfer.objects.latest('id')
        self.assertEqual(saved_second_transfer.amount, second_form_input['amount'])
        self.assertEqual(saved_second_transfer.user_id, second_form_input['user_id'])
        self.assertEqual(saved_second_transfer.lesson_id, second_form_input['lesson_id'])

    def test_student_can_make_multiple_transfers_for_same_lesson(self):
        transfer_form = TransferForm(data=self.form_input)
        transfer_count_before = Transfer.objects.count()
        transfer_form.save()
        second_form_input = {
            'amount': 100.00,
            'user_id': 1,
            'lesson_id': 1
        }
        second_transfer_form = TransferForm(data=second_form_input)
        second_transfer_form.save()
        transfer_count_after = Transfer.objects.count()
        self.assertEqual(transfer_count_before + 2, transfer_count_after)
        saved_second_transfer = Transfer.objects.latest('id')
        self.assertEqual(saved_second_transfer.amount, second_form_input['amount'])
        self.assertEqual(saved_second_transfer.user_id, second_form_input['user_id'])
        self.assertEqual(saved_second_transfer.lesson_id, second_form_input['lesson_id'])

    def test_invalid_if_user_not_found(self):
        self.form_input['user_id'] = 999
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_if_lesson_not_found(self):
        self.form_input['lesson_id'] = 999
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_if_lesson_not_booked_by_user(self):
        self.form_input['lesson_id'] = 3
        form = TransferForm(data=self.form_input)
        self.assertFalse(form.is_valid())