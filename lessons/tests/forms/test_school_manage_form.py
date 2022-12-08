from django import forms
from django.test import TestCase
from lessons.forms import SchoolManageForm
from lessons.models import User, School


class SchoolManageFormTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        self.user = User.objects.get(first_name='Foo')
        self.school = School.objects.get(id=1)
        self.form_input = {
            'name': 'School',
            'description': 'Music Lesson',
            'delete_school': False
        }

    def test_form_contains_required_fields(self):
        form = SchoolManageForm()
        self.assertIn('name', form.fields)
        self.assertIn('description', form.fields)
        name_field = form.fields['name']
        self.assertTrue(isinstance(name_field, forms.CharField))
        description_field = form.fields['description']
        self.assertTrue(isinstance(description_field, forms.CharField))
        delete_school_field = form.fields['delete_school']
        self.assertTrue(isinstance(delete_school_field, forms.BooleanField))

    def test_form_saves_correctly(self):
        form = SchoolManageForm(instance=self.school, data=self.form_input)
        school_count_before = School.objects.count()
        school = form.save(commit=False)
        school.director = self.user
        school.save()
        school_count_after = School.objects.count()
        self.assertEqual(school_count_before, school_count_after)
        saved_school = School.objects.get(name=self.form_input['name'])
        self.assertEqual(saved_school.name, self.form_input['name'])
        self.assertEqual(saved_school.description, self.form_input['description'])
