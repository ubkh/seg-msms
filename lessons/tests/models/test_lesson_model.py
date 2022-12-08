"""
Tests that will be used to test the Lesson model.
"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from lessons.models import Lesson, User


class LessonModelTestCase(TestCase):
    """
    Unit tests that will be used to test the Lesson model.
    """

    fixtures = ['lessons/tests/fixtures/default_user.json', 'lessons/tests/fixtures/default_lesson.json',
                'lessons/tests/fixtures/other_lesson.json', 'lessons/tests/fixtures/default_school.json']

    def setUp(self):
        self.user = User.objects.get(first_name='Foo')
        self.lesson = Lesson.objects.get(title='Test Lesson')
        self.other_lesson = Lesson.objects.get(title='Test Lesson 2')

    def _assert_lesson_is_valid(self, lesson):
        try:
            lesson.full_clean()
        except ValidationError:
            self.fail("Lesson is not valid.")

    def _assert_lesson_is_invalid(self, lesson):
        with self.assertRaises(ValidationError):
            lesson.full_clean()

    """
    Test user
    """

    def test_lesson_is_valid(self):
        self._assert_lesson_is_valid(self.lesson)

    """
    Test Title
    """

    def test_title_cannot_be_empty(self):
        self.lesson.title = ''
        self._assert_lesson_is_invalid(self.lesson)

    def test_title_can_be_same(self):
        self.other_lesson.title = 'Test Lesson'
        self._assert_lesson_is_valid(self.other_lesson)
        self._assert_lesson_is_valid(self.lesson)

    def test_title_can_be_25_characters(self):
        self.lesson.title = 'a' * 25
        self._assert_lesson_is_valid(self.lesson)

    def test_title_cannot_be_greater_than_25_characters(self):
        self.lesson.title = 'a' * 26
        self._assert_lesson_is_invalid(self.lesson)

    def test_title_can_contain_numbers(self):
        self.lesson.title = 'Lesson 1'
        self._assert_lesson_is_valid(self.lesson)

    def test_title_can_contain_special_characters(self):
        self.lesson.title = '#Lesson 1 $5'
        self._assert_lesson_is_valid(self.lesson)

    """
    Test Information
    """

    def test_information_can_be_empty(self):
        self.lesson.information = ''
        self._assert_lesson_is_valid(self.lesson)

    def test_information_can_be_same(self):
        self.lesson.information = 'Test'
        self.other_lesson.information = 'Test'
        self._assert_lesson_is_valid(self.other_lesson)
        self._assert_lesson_is_valid(self.lesson)

    def test_information_can_be_280_characters(self):
        self.lesson.lesson = 'a' * 280
        self._assert_lesson_is_valid(self.lesson)

    def test_information_cannot_be_greater_than_280_characters(self):
        self.lesson.information = 'a' * 281
        self._assert_lesson_is_invalid(self.lesson)

    def test_information_can_contain_numbers(self):
        self.lesson.information = 'Lesson 1'
        self._assert_lesson_is_valid(self.lesson)

    def test_information_can_contain_special_characters(self):
        self.lesson.information = '#Lesson 1 $5'
        self._assert_lesson_is_valid(self.lesson)

    """
    Test Day Field
    """

    def test_day_cannot_be_empty(self):
        self.lesson.day = ''
        self._assert_lesson_is_invalid(self.lesson)

    def test_day_cannot_be_lowercase(self):
        self.lesson.day = 'monday'
        self._assert_lesson_is_invalid(self.lesson)

    def test_day_cannot_be_uppercase(self):
        self.lesson.day = 'MONDAY'
        self._assert_lesson_is_invalid(self.lesson)

    def test_day_cannot_contain_numbers(self):
        self.lesson.day = 'Monday 1'
        self._assert_lesson_is_invalid(self.lesson)

    def test_day_cannot_contain_spaces(self):
        self.lesson.day = 'Mon day'
        self._assert_lesson_is_invalid(self.lesson)

    def test_day_cannot_contain_special_characters(self):
        self.lesson.day = '#Monday@'
        self._assert_lesson_is_invalid(self.lesson)

    def test_day_can_be_the_same(self):
        self.lesson.day = 'Monday'
        self.other_lesson.day = 'Monday'
        self._assert_lesson_is_valid(self.lesson)
        self._assert_lesson_is_valid(self.other_lesson)

    def test_day_can_be_weekend(self):
        self.lesson.day = 'Sunday'
        self._assert_lesson_is_valid(self.lesson)

    def test_day_cannot_be_made_up(self):
        self.lesson.day = 'Testday'
        self._assert_lesson_is_invalid(self.lesson)

    """
    Test Instrument Field
    """

    def test_instrument_cannot_be_empty(self):
        self.lesson.instrument = ''
        self._assert_lesson_is_invalid(self.lesson)

    def test_instrument_cannot_be_lowercase(self):
        self.lesson.instrument = 'piano'
        self._assert_lesson_is_invalid(self.lesson)

    def test_instrument_cannot_be_uppercase(self):
        self.lesson.instrument = 'PIANO'
        self._assert_lesson_is_invalid(self.lesson)

    def test_instrument_cannot_contain_numbers(self):
        self.lesson.instrument = 'Piano 1'
        self._assert_lesson_is_invalid(self.lesson)

    def test_instrument_cannot_contain_spaces(self):
        self.lesson.instrument = 'Pi ano'
        self._assert_lesson_is_invalid(self.lesson)

    def test_instrument_cannot_contain_special_characters(self):
        self.lesson.instrument = '#Piano@'
        self._assert_lesson_is_invalid(self.lesson)

    def test_instrument_can_be_the_same(self):
        self.lesson.instrument = 'Piano'
        self.other_lesson.instrument = 'Piano'
        self._assert_lesson_is_valid(self.lesson)
        self._assert_lesson_is_valid(self.other_lesson)

    def test_instrument_cannot_be_made_up(self):
        self.lesson.day = 'MadeUpInstrument'
        self._assert_lesson_is_invalid(self.lesson)

    """
    Test Duration
    """

    def test_duration_cannot_be_zero(self):
        self.lesson.duration = 0
        self._assert_lesson_is_invalid(self.lesson)

    def test_duration_cannot_be_negative(self):
        self.lesson.duration = -60
        self._assert_lesson_is_invalid(self.lesson)

    def test_duration_cannot_be_fractional(self):
        self.lesson.duration = 41.3
        self._assert_lesson_is_invalid(self.lesson)

    def test_duration_30_minimum(self):
        self.lesson.duration = 30
        self._assert_lesson_is_valid(self.lesson)

    def test_duration_cannot_be_less_than_30(self):
        self.lesson.duration = 15
        self._assert_lesson_is_invalid(self.lesson)

    def test_duration_uses_steps_of_15(self):
        self.lesson.duration = 45
        self._assert_lesson_is_valid(self.lesson)
        self.lesson.duration = 51
        self._assert_lesson_is_invalid(self.lesson)

    def test_duration_60_maximum(self):
        self.lesson.duration = 60
        self._assert_lesson_is_valid(self.lesson)

    def test_duration_cannot_be_greater_than_60(self):
        self.lesson.duration = 75
        self._assert_lesson_is_invalid(self.lesson)

    def test_duration_can_be_the_same(self):
        self.lesson.duration = 30
        self.other_lesson.duration = 30
        self._assert_lesson_is_valid(self.lesson)
        self._assert_lesson_is_valid(self.other_lesson)

    """
    Test Interval
    """

    def test_interval_cannot_be_zero(self):
        self.lesson.interval = 0
        self._assert_lesson_is_invalid(self.lesson)

    def test_interval_1_minimum(self):
        self.lesson.interval = 1
        self._assert_lesson_is_valid(self.lesson)

    def test_interval_4_maximum(self):
        self.lesson.interval = 4
        self._assert_lesson_is_valid(self.lesson)

    def test_interval_cannot_be_greater_thant_4(self):
        self.lesson.interval = 5
        self._assert_lesson_is_invalid(self.lesson)

    def test_interval_can_be_the_same(self):
        self.lesson.interval = 1
        self.other_lesson.interval = 1
        self._assert_lesson_is_valid(self.lesson)
        self._assert_lesson_is_valid(self.other_lesson)

    """
    Test Price Field
    """

    def test_price_cannot_be_zero(self):
        self.lesson.price = 0
        self._assert_lesson_is_invalid(self.lesson)

    def test_price_cannot_be_negative(self):
        self.lesson.price = -5.00
        self._assert_lesson_is_invalid(self.lesson)

    def test_price_can_be_fractional(self):
        self.lesson.price = 10.50
        self._assert_lesson_is_valid(self.lesson)

    def test_price_5_minimum(self):
        self.lesson.price = 5.00
        self._assert_lesson_is_valid(self.lesson)

    def test_price_cannot_be_less_than_5(self):
        self.lesson.price = 4.00
        self._assert_lesson_is_invalid(self.lesson)

    def test_price_can_be_the_same(self):
        self.lesson.price = 10.00
        self.other_lesson.price = 10.00
        self._assert_lesson_is_valid(self.lesson)
        self._assert_lesson_is_valid(self.other_lesson)
