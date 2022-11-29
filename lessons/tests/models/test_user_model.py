"""
Tests that will be used to test the User model.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from lessons.models import User
from lessons.tests.helpers import LoginTester


# Create your tests here.

class UserModelTestCase(TestCase, LoginTester):
    """
    Unit tests that will be used to test the User model.
    """
    fixtures = [
        'lessons/tests/fixtures/default_user.json',
        'lessons/tests/fixtures/other_user.json',
    ]

    def setUp(self):
        self.user = self._create_user()
        self.secondary_user = self._create_secondary_user()

    def _create_user(self):
        user = User.objects.get(first_name='Foo')
        return user

    def _create_secondary_user(self):
        user = User.objects.get(first_name='Doe')
        return user

    def _assert_user_is_valid(self, user):
        try:
            user.full_clean()
        except ValidationError:
            self.fail("User is not valid.")

    def _assert_user_is_invalid(self, user):
        with self.assertRaises(ValidationError):
            user.full_clean()

    """
    Test user
    """

    def test_user_is_valid(self):
        self._assert_user_is_valid(self.user)

    """
    Test Reference Number/ ID
    """

    def test_id_is_unique(self):
        self.assertNotEqual(self.secondary_user.id, self.user.id)

    def test_first_id(self):
        self.assertEqual(self.user.id, 1)

    """
    Test e-mail
    """

    def test_email_can_equal_254_characters(self):
        # As according to RFC 3696
        self.user.email = 'a' * 248 + '@b.com'
        self.assertEqual(len(self.user.email), 254)
        self._assert_user_is_valid(self.user)

    def test_email_cannot_exceed_254_characters(self):
        # As according to RFC 3696
        self.user.email = 'a' * 249 + '@b.com'
        self.assertEqual(len(self.user.email), 255)
        self._assert_user_is_invalid(self.user)

    def test_email_cannot_be_blank(self):
        self.user.email = ''
        self._assert_user_is_invalid(self.user)

    def test_email_must_be_unique(self):
        self.user.email = self.secondary_user.email
        self._assert_user_is_invalid(self.user)

    def test_email_with_different_case_must_be_unique(self):
        # As according to RFC 5321
        self.user.email = self.secondary_user.email.upper()
        self._assert_user_is_valid(self.user)

    def test_email_must_contain_local_part(self):
        self.user.email = '@kangaroo.com'
        self._assert_user_is_invalid(self.user)

    def test_email_must_contain_symbol_at(self):
        self.user.email = 'bar-kangaroo.com'
        self._assert_user_is_invalid(self.user)

    def test_email_must_contain_domain(self):
        self.user.email = 'bar@.com'
        self._assert_user_is_invalid(self.user)

    def test_email_must_contain_top_level_domain(self):
        self.user.email = 'bar@kangaroo'
        self._assert_user_is_invalid(self.user)

    def test_email_cannot_contain_symbol_at_duplicates(self):
        self.user.email = 'foo@@kangaroo.com'
        self._assert_user_is_invalid(self.user)

    """
    Test first name
    """

    def test_first_name_can_equal_40_characters(self):
        self.user.first_name = 'a' * 40
        self._assert_user_is_valid(self.user)

    def test_first_name_cannot_exceed_41_characters(self):
        self.user.first_name = 'a' * 41
        self._assert_user_is_invalid(self.user)

    def test_first_name_cannot_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid(self.user)

    def test_first_name_does_not_have_to_be_unique(self):
        self.user.first_name = self.secondary_user.first_name
        self._assert_user_is_valid(self.user)

    def test_first_name_can_have_spaces(self):
        self.user.first_name = "Foo Kangaroo"
        self._assert_user_is_valid(self.user)

    def test_first_name_can_have_hyphens(self):
        self.user.first_name = "Foo-Kangaroo"
        self._assert_user_is_valid(self.user)

    def test_first_name_can_have_diacritics(self):
        self.user.first_name = "ÁáÀÂàÂâÄäÃãÅåÆæÇçÐðÉéÈèÊêËëÍíÌìÎîÏï"
        self._assert_user_is_valid(self.user)

    def test_first_name_cannot_contain_non_latin_scripts(self):
        for name in ['համար', 'التركيز', 'елементарен', '最近', 'საბეჭდი', 'απλά', 'מוסחת', 'और', 'เนื้อหา', 'இப்சம்']:
            self.user.first_name = name
            self._assert_user_is_invalid(self.user)

    def test_first_name_cannot_have_numbers(self):
        for digit in range(0, 10):
            self.user.first_name = str(digit)
            self._assert_user_is_invalid(self.user)

    def test_first_name_cannot_have_symbols(self):
        for symbol in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>',
                       '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨',
                       '©', '«', '¬', '®', '¯', '°', '±', '´', '¶', '·', '¸', '»', '¿', '\\']:
            self.user.first_name = symbol
            self._assert_user_is_invalid(self.user)

    """
    Test last name
    """

    def test_last_name_can_equal_40_characters(self):
        self.user.last_name = 'a' * 40
        self._assert_user_is_valid(self.user)

    def test_last_name_cannot_exceed_41_characters(self):
        self.user.last_name = 'a' * 41
        self._assert_user_is_invalid(self.user)

    def test_last_name_cannot_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid(self.user)

    def test_last_name_does_not_have_to_be_unique(self):
        self.user.last_name = self.secondary_user.last_name
        self._assert_user_is_valid(self.user)

    def test_last_name_can_have_spaces(self):
        self.user.last_name = "Foo Kangaroo"
        self._assert_user_is_valid(self.user)

    def test_last_name_can_have_hyphens(self):
        self.user.last_name = "Foo-Kangaroo"
        self._assert_user_is_valid(self.user)

    def test_last_name_can_have_diacritics(self):
        self.user.last_name = "ÁáÀÂàÂâÄäÃãÅåÆæÇçÐðÉéÈèÊêËëÍíÌìÎîÏï"
        self._assert_user_is_valid(self.user)

    def test_last_name_cannot_contain_non_latin_scripts(self):
        for name in ['համար', 'التركيز', 'елементарен', '最近', 'საბეჭდი', 'απλά', 'מוסחת', 'और', 'เนื้อหา', 'இப்சம்']:
            self.user.last_name = name
            self._assert_user_is_invalid(self.user)

    def test_last_name_cannot_have_numbers(self):
        for digit in range(0, 10):
            self.user.last_name = str(digit)
            self._assert_user_is_invalid(self.user)

    def test_last_name_cannot_have_symbols(self):
        for symbol in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '.', '/', ':', ';', '<', '=', '>',
                       '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨',
                       '©', '«', '¬', '®', '¯', '°', '±', '´', '¶', '·', '¸', '»', '¿', '\\']:
            self.user.last_name = symbol
            self._assert_user_is_invalid(self.user)
