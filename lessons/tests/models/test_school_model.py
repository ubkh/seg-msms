"""
Tests that will be used to test the School model.
"""
from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import User, School


class SchoolModelTestCase(TestCase):
    """
    Unit tests that will be used to test the School model.
    """
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.school = School.objects.get(id=1)

    def _assert_school_is_valid(self, school):
        try:
            school.full_clean()
        except ValidationError:
            self.fail("School is not valid.")

    def _assert_school_is_invalid(self, school):
        with self.assertRaises(ValidationError):
            school.full_clean()

    """
    Test School
    """

    def test_school_is_valid(self):
        self._assert_school_is_valid(self.user)

    """
    Test name
    """

    def test_name_cannot_be_blank(self):
        self.school.name = ""
        self._assert_school_is_invalid(self.school)

    def test_name_can_have_one_character(self):
        self.school.name = "a"
        self._assert_school_is_valid(self.school)

    def test_name_can_have_30_characters(self):
        self.school.name = "a" * 30
        self._assert_school_is_valid(self.school)

    def test_name_cannot_have_more_than_30_characters(self):
        self.school.name = "a" * 31
        self._assert_school_is_invalid(self.school)

    """
    Test Director
    """

    def test_director_cannot_be_blank(self):
        self.school.director = None
        self._assert_school_is_invalid(self.school)

    """
    Test Current Term
    """

    def test_current_term_can_be_blank(self):
        self.school.current_term = None
        self._assert_school_is_valid(self.school)

    """
    Test Clients
    """

    def test_clients_can_be_blank(self):
        self.school.clients.clear()
        self._assert_school_is_valid(self.school)

    def test_clients_can_have_one_member(self):
        user = User(first_name="A", last_name="B", email="a@b.com")
        user.save()
        self.school.clients.add(user)
        self._assert_school_is_valid(self.school)

    def test_clients_can_have_multiple_members(self):
        first_user = User(first_name="A", last_name="B", email="a@b.com")
        first_user.save()
        second_user = User(first_name="C", last_name="D", email="c@d.com")
        second_user.save()
        self.school.clients.add(first_user)
        self.school.clients.add(second_user)
        self._assert_school_is_valid(self.school)

    def test_clients_can_have_director_as_member(self):
        self.school.clients.add(self.user)
        self._assert_school_is_valid(self.school)

    """
    Test Description
    """

    def test_description_cannot_be_blank(self):
        self.school.description = ""
        self._assert_school_is_invalid(self.school)

    def test_description_can_have_one_or_more_characters(self):
        self.school.description = "a"
        self._assert_school_is_valid(self.school)

    def test_description_can_have_1000_or_more_characters(self):
        self.school.description = "a" * 1000
        self._assert_school_is_valid(self.school)

    def test_description_can_have_10000_or_more_characters(self):
        self.school.description = "a" * 10000
        self._assert_school_is_valid(self.school)
