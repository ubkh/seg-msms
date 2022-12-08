from unittest import TestCase

from django import forms

from lessons.forms import ManageMemberForm


class ManageMemberFormTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.form_input = self._create_form_input()


    def _create_form_input(self):
        form_input = {
            'client': False,
            'teacher': False,
            'administrator': False,
            'super_administrator': False,
            'ban_member': False
        }
        return form_input

    def test_manage_member_form_is_valid(self):
        manage_member_form = ManageMemberForm(data=self.form_input)
        self.assertTrue(manage_member_form.is_valid())

    def test_member_modify_form_contains_required_fields(self):
        manage_member_form = ManageMemberForm(data=self.form_input)
        self.assertIn('client', manage_member_form.fields)
        client_field = manage_member_form.fields['client']
        self.assertTrue(isinstance(client_field, forms.BooleanField))
        self.assertIn('teacher', manage_member_form.fields)
        teacher_field = manage_member_form.fields['teacher']
        self.assertTrue(isinstance(teacher_field, forms.BooleanField))
        self.assertIn('administrator', manage_member_form.fields)
        administrator_field = manage_member_form.fields['administrator']
        self.assertTrue(isinstance(administrator_field, forms.BooleanField))
        self.assertIn('super_administrator', manage_member_form.fields)
        super_administrator_field = manage_member_form.fields['super_administrator']
        self.assertTrue(isinstance(super_administrator_field, forms.BooleanField))
        self.assertIn('ban_member', manage_member_form.fields)
        ban_member_field = manage_member_form.fields['ban_member']
        self.assertTrue(isinstance(ban_member_field, forms.BooleanField))


    def test_client_can_be_true(self):
        self.form_input['client'] = True
        form = ManageMemberForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_teacher_can_be_true(self):
        self.form_input['teacher'] = True
        form = ManageMemberForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_administrator_can_be_true(self):
        self.form_input['administrator'] = True
        form = ManageMemberForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_super_administrator_can_be_true(self):
        self.form_input['super_administrator'] = True
        form = ManageMemberForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_ban_member_can_be_true(self):
        self.form_input['ban_member'] = True
        form = ManageMemberForm(data=self.form_input)
        self.assertTrue(form.is_valid())
