from django.test import TestCase

from django.urls import reverse

from lessons.models import User, School


class SchoolHomeViewTestCase(TestCase):

    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json',
    ]

    def setUp(self):
        self.school = School.objects.get(id=1)
        self.url = reverse('school_home', kwargs={'school': self.school.id})
        self.user = User.objects.get(email='foo@kangaroo.com')

    def test_display_school_home_url(self):
        self.assertEqual(self.url, f'/school/{self.school.id}/')

    def test_get_school_home(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/home.html')
        self.assertContains(response, self.school.name)
