from django.test import TestCase
from django import forms

from lessons.forms import AdminModifyForm
from lessons.models import User


class AdminModifyFormTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.form_input = self._create_form_input()

    def _create_form_input(self):
        form_input = {
            'first_name': 'Baz',
            'last_name': 'Dab',
            'email': 'baz@kangaroo.com',
            'make_account_super_administrator': 'False',
            'delete_account': 'False'
        }
        return form_input

    def test_admin_modify_form_is_valid(self):
        register_form = AdminModifyForm(data=self.form_input)
        self.assertTrue(register_form.is_valid())

    def test_admin_modify_form_contains_required_fields(self):
        admin_modify_form = AdminModifyForm()
        self.assertIn('first_name', admin_modify_form.fields)
        first_name_field = admin_modify_form.fields['first_name']
        self.assertTrue(isinstance(first_name_field, forms.CharField))
        self.assertIn('last_name', admin_modify_form.fields)
        last_name_field = admin_modify_form.fields['last_name']
        self.assertTrue(isinstance(last_name_field, forms.CharField))
        self.assertIn('email', admin_modify_form.fields)
        email_field = admin_modify_form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('make_account_super_administrator', admin_modify_form.fields)
        make_account_super_administrator_field = admin_modify_form.fields['make_account_super_administrator']
        self.assertTrue(isinstance(make_account_super_administrator_field, forms.BooleanField))
        self.assertIn('delete_account', admin_modify_form.fields)
        delete_account_field = admin_modify_form.fields['delete_account']
        self.assertTrue(isinstance(delete_account_field, forms.BooleanField))

    def test_form_saves_correctly(self):
        user = User.objects.get(email='foo@kangaroo.com')
        admin_modify_form = AdminModifyForm(instance=user, data=self.form_input)
        user_count_before = User.objects.count()
        admin_modify_form.save()
        user_count_after = User.objects.count()
        self.assertEqual(user_count_before, user_count_after)
        self.assertEqual(user.first_name, self.form_input['first_name'])
        self.assertEqual(user.last_name, self.form_input['last_name'])
        self.assertEqual(user.email, self.form_input['email'])

    def test_form_uses_model_email_validation(self):
        self.form_input['email'] = 'kangaroo.com'
        form = AdminModifyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_model_first_name_validation(self):
        self.form_input['first_name'] = 'n@me'
        form = AdminModifyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_uses_model_last_name_validation(self):
        self.form_input['last_name'] = 'n@me'
        form = AdminModifyForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_make_account_super_administrator_can_be_true(self):
        self.form_input['make_account_super_administrator'] = 'True'
        form = AdminModifyForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_delete_account_can_be_true(self):
        self.form_input['delete_account'] = 'True'
        form = AdminModifyForm(data=self.form_input)
        self.assertTrue(form.is_valid())
