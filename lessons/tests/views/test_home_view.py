from django.test import TestCase

from django.urls import reverse

from lessons.models import User, School


class HomeViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        self.school = School.objects.get(id=1)
        self.url = reverse('home')
        self.user = User.objects.get(email='foo@kangaroo.com')

    def test_display_home_url(self):
        self.assertEqual(self.url, f'/home/')

    def test_get_home(self):
        self.client.login(email=self.user.email, password="Password123")
        second_school = School(director=self.user, name="New School", description="Test")
        second_school.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'school/list_school.html')
        self.assertContains(response, self.school.name)
        self.assertContains(response, second_school.name)
