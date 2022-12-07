"""
Tests that will be used to test the Admission mixin.
"""
from django.test import TestCase

from lessons.models import User, School, Admission


class AdmissionMixinTestCase(TestCase):
    """
    Unit tests that will be used to test the Admission mixin.
    """
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        super(TestCase, self).setUp()
        self.user = User.objects.get(email='foo@kangaroo.com')
        self.school = School.objects.get(id=1)

    def _group_list(self, school, user):
        group_list = []
        admission = Admission.objects.get(client=user, school=school)
        for group in admission.groups.all():
            group_list.append(group.name)
        return group_list

    """
    Test member functions
    """

    def test_leave_school(self):
        self.school.set_group_client(self.user)
        self.assertTrue(self.school.has_member(self.user))
        self.school.leave_school(self.user)
        self.assertFalse(self.school.has_member(self.user))

    def test_ban_member(self):
        self.school.set_group_client(self.user)
        self.assertFalse(self.school.get_ban(self.user))
        self.school.ban_member(self.user)
        self.assertTrue(self.school.get_ban(self.user))

    def test_unban_member(self):
        self.school.set_group_client(self.user)
        self.school.ban_member(self.user)
        self.assertTrue(self.school.get_ban(self.user))
        self.school.unban_member(self.user)
        self.assertFalse(self.school.get_ban(self.user))

    def test_has_member(self):
        self.assertFalse(self.school.is_client(self.user))
        self.school.set_group_client(self.user)
        self.assertTrue(self.school.is_client(self.user))

    def test_get_ban(self):
        self.school.set_group_client(self.user)
        admission = Admission.objects.get(client=self.user, school=self.school)
        admission.is_active = True
        admission.save()
        self.assertFalse(self.school.get_ban(self.user))
        admission.is_active = False
        admission.save()
        self.assertTrue(self.school.get_ban(self.user))

    """
    Test group getters
    """

    def test_is_director(self):
        self.assertFalse(self.school.is_director(self.user))
        self.school.set_group_director(self.user)
        self.assertTrue(self.school.is_director(self.user))

    def test_is_super_administrator(self):
        self.assertFalse(self.school.is_super_administrator(self.user))
        self.school.set_group_super_administrator(self.user)
        self.assertTrue(self.school.is_super_administrator(self.user))

    def test_is_administrator(self):
        self.assertFalse(self.school.is_administrator(self.user))
        self.school.set_group_administrator(self.user)
        self.assertTrue(self.school.is_administrator(self.user))

    def test_is_teacher(self):
        self.assertFalse(self.school.is_teacher(self.user))
        self.school.set_group_teacher(self.user)
        self.assertTrue(self.school.is_teacher(self.user))

    def test_is_client(self):
        self.assertFalse(self.school.is_client(self.user))
        self.school.set_group_client(self.user)
        self.assertTrue(self.school.is_client(self.user))

    """
    Test group setters
    """

    def test_set_group_director(self):
        self.school.set_group_director(self.user)
        group_list = self._group_list(self.school, self.user)
        self.assertIn("Director", group_list)
        self.assertIn("Super-administrator", group_list)
        self.assertIn("Administrator", group_list)
        self.assertNotIn("Teacher", group_list)
        self.assertNotIn("Client", group_list)
        self.assertEqual(len(group_list), 3)

    def test_set_group_super_administrator(self):
        self.school.set_group_super_administrator(self.user)
        group_list = self._group_list(self.school, self.user)
        self.assertNotIn("Director", group_list)
        self.assertIn("Super-administrator", group_list)
        self.assertIn("Administrator", group_list)
        self.assertNotIn("Teacher", group_list)
        self.assertNotIn("Client", group_list)
        self.assertEqual(len(group_list), 2)

    def test_set_group_administrator(self):
        self.school.set_group_administrator(self.user)
        group_list = self._group_list(self.school, self.user)
        self.assertNotIn("Director", group_list)
        self.assertNotIn("Super-administrator", group_list)
        self.assertIn("Administrator", group_list)
        self.assertNotIn("Teacher", group_list)
        self.assertNotIn("Client", group_list)
        self.assertEqual(len(group_list), 1)

    def test_set_group_teacher(self):
        self.school.set_group_teacher(self.user)
        group_list = self._group_list(self.school, self.user)
        self.assertNotIn("Director", group_list)
        self.assertNotIn("Super-administrator", group_list)
        self.assertNotIn("Administrator", group_list)
        self.assertIn("Teacher", group_list)
        self.assertNotIn("Client", group_list)
        self.assertEqual(len(group_list), 1)

    def test_set_group_client(self):
        self.school.set_group_client(self.user)
        group_list = self._group_list(self.school, self.user)
        self.assertNotIn("Director", group_list)
        self.assertNotIn("Super-administrator", group_list)
        self.assertNotIn("Administrator", group_list)
        self.assertNotIn("Teacher", group_list)
        self.assertIn("Client", group_list)
        self.assertEqual(len(group_list), 1)
