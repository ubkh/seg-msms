"""
Tests that will be used to test the Admission model.
"""
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import User, School, Admission


class AdmissionModelTestCase(TestCase):
    """
    Unit tests that will be used to test the Admission model.
    """
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.school = School.objects.get(id=1)
        self.admission = Admission(school=self.school, client=self.user)

    def _assert_admission_is_valid(self, admission):
        try:
            admission.full_clean()
        except ValidationError:
            self.fail("School is not valid.")

    def _assert_admission_is_invalid(self, admission):
        with self.assertRaises(ValidationError):
            admission.full_clean()

    """
    Test admission
    """

    def test_admission_is_valid(self):
        self._assert_admission_is_valid(self.admission)

    """
    Test school
    """

    def test_school_cannot_be_blank(self):
        self.admission.school = None
        self._assert_admission_is_invalid(self.admission)

    """
    Test client
    """

    def test_client_cannot_be_blank(self):
        self.admission.client = None
        self._assert_admission_is_invalid(self.admission)

    """
    Test groups
    """

    def test_groups_can_be_blank(self):
        self.admission.save()
        self.admission.groups.clear()
        self._assert_admission_is_valid(self.admission)

    def test_groups_can_have_single_group(self):
        self.admission.save()
        group, created = Group.objects.get_or_create(name="Group A")
        self.admission.groups.add(group)
        self._assert_admission_is_valid(self.admission)

    def test_groups_can_have_multiple_groups(self):
        self.admission.save()
        group_a, created = Group.objects.get_or_create(name="Group A")
        self.admission.groups.add(group_a)
        group_b, created = Group.objects.get_or_create(name="Group B")
        self.admission.groups.add(group_b)
        self._assert_admission_is_valid(self.admission)

    """
    Test is active
    """

    def test_can_be_active(self):
        self.admission.is_active = True
        self._assert_admission_is_valid(self.admission)

    def test_can_be_not_active(self):
        self.admission.is_active = False
        self._assert_admission_is_valid(self.admission)

    def test_active_default_is_true(self):
        # As active field was not defined at creation
        self.assertEqual(self.admission.is_active, True)
