from django.test import TestCase
from django.urls import reverse

from lessons.models import User, School


class DisplayTeacherTimetableViewTestCase(TestCase):
    fixtures = [
        'lessons/tests/fixtures/default_teacher.json',
        'lessons/tests/fixtures/default_school.json'
    ]

    def setUp(self):
        self.school = School.objects.get(id=1)
        self.url = reverse('teacher_timetable', kwargs={'school': self.school.id})
        self.user = User.objects.get(email='camus@kangaroo.com')
        self.school.set_group_teacher(self.user)

    def test_teacher_url(self):
        self.assertEqual(self.url, f'/school/{self.school.id}/teacher/timetable/')

    def test_get_teacher(self):
        self.client.login(email=self.user.email, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'timetable/timetable.html')
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)