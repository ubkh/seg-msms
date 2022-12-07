"""
Tests that will be used to test the Transfer model.
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import User, Lesson, Transfer, School


class TransferModelTestCase(TestCase):
    """
    Unit tests that will be used to test the Transfer model.
    """

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_lesson.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.lesson = Lesson.objects.get(pk=1)
        self.school = School.objects.get(pk=1)
        self.transfer = Transfer(
            user=self.user,
            lesson=self.lesson,
            school=self.school,
            amount='100.00'
        )

    def _assert_transfer_is_valid(self, transfer):
        try:
            transfer.full_clean()
        except ValidationError:
            self.fail("Transfer is not valid.")

    def _assert_transfer_is_invalid(self, transfer):
        with self.assertRaises(ValidationError):
            transfer.full_clean()

    """
    Test Transfer
    """

    def test_transfer_is_valid(self):
        self._assert_transfer_is_valid(self.transfer)

    """
    Test User
    """

    def test_user_must_not_be_blank(self):
        self.transfer.user = None
        self._assert_transfer_is_invalid(self.transfer)

    """
    Test School
    """

    def test_school_must_not_be_blank(self):
        self.transfer.school = None
        self._assert_transfer_is_invalid(self.transfer)

    """
    Test Lesson
    """

    def test_lesson_must_not_be_blank(self):
        self.transfer.lesson = None
        self._assert_transfer_is_invalid(self.transfer)

    """
    Test Amount
    """

    def test_amount_must_not_be_negative(self):
        self.transfer.amount = '-0.01'
        self._assert_transfer_is_invalid(self.transfer)

    def test_amount_must_not_be_zero(self):
        self.transfer.amount = '0.00'
        self._assert_transfer_is_invalid(self.transfer)

    def test_amount_must_be_greater_than_zero(self):
        self.transfer.amount = '0.01'
        self._assert_transfer_is_valid(self.transfer)

    def test_amount_can_have_eight_digits(self):
        self.transfer.amount = '999999.99'
        self._assert_transfer_is_valid(self.transfer)

    def test_amount_cannot_have_nine_or_more_digits(self):
        self.transfer.amount = '1000000.00'
        self._assert_transfer_is_invalid(self.transfer)

    def test_amount_can_have_zero_decimal_places(self):
        self.transfer.amount = '1'
        self._assert_transfer_is_valid(self.transfer)

    def test_amount_can_have_one_decimal_places(self):
        self.transfer.amount = '0.1'
        self._assert_transfer_is_valid(self.transfer)

    def test_amount_can_have_two_decimal_places(self):
        self.transfer.amount = '0.12'
        self._assert_transfer_is_valid(self.transfer)

    def test_amount_cannot_have_three_or_more_decimal_places(self):
        self.transfer.amount = '0.123'
        self._assert_transfer_is_invalid(self.transfer)
