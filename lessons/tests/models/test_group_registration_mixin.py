"""
Tests that will be used to test the Group Registration mixin.
"""
from django.test import TestCase

from lessons.models import User


class GroupRegistrationMixinTestCase(TestCase):
    """
    Unit tests that will be used to test the Group Registration mixin.
    """
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='foo@kangaroo.com')

    def _group_list(self, user):
        group_list = []
        for group in user.groups.all():
            group_list.append(group.name)
        return group_list

    """
    Test set group
    """

    def test_set_group_system_administrator(self):
        self.user.set_group_system_administrator()
        group_list = self._group_list(self.user)
        self.assertIn("System-administrator", group_list)
        self.assertNotIn("Director", group_list)
        self.assertNotIn("Adult-user", group_list)
        self.assertNotIn("User", group_list)
        self.assertEqual(len(group_list), 1)

    def test_set_group_director(self):
        self.user.set_group_director()
        group_list = self._group_list(self.user)
        self.assertNotIn("System-administrator", group_list)
        self.assertIn("Director", group_list)
        self.assertIn("Adult-user", group_list)
        self.assertIn("User", group_list)
        self.assertEqual(len(group_list), 3)

    def test_set_group_adult_user(self):
        self.user.set_group_adult_user()
        group_list = self._group_list(self.user)
        self.assertNotIn("System-administrator", group_list)
        self.assertNotIn("Director", group_list)
        self.assertIn("Adult-user", group_list)
        self.assertIn("User", group_list)
        self.assertEqual(len(group_list), 2)

    def test_set_group_user(self):
        self.user.set_group_user()
        group_list = self._group_list(self.user)
        self.assertNotIn("System-administrator", group_list)
        self.assertNotIn("Director", group_list)
        self.assertNotIn("Adult-user", group_list)
        self.assertIn("User", group_list)
        self.assertEqual(len(group_list), 1)
