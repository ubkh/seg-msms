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
    fixtures = ['lessons/tests/fixtures/default_user.json']
    
    def setUp(self):
        self.user = self._create_user()
        self.secondary_user = self._create_secondary_user()

    def _create_user(self):
        user = User.objects.get(name='Foo Bar')
        return user

    def _create_secondary_user(self):
        user = User.objects.get(name='Doe Ball')
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

    def test_email_must_contain_local_part(self):
        self.user.email = '@kangaroo.com'
        self._assert_user_is_invalid(self.user)

    def test_email_must_contain_symbol_at(self):
        self.user.email = 'bar-kangaroo.com'
        self._assert_user_is_invalid(self.user)

    def test_email_must_contain_domain(self):
        self.user.email = 'bar@.com'
        self._assert_user_is_invalid(self.user)

    def test_email_must_contain_top_leveldomain(self):
        self.user.email = 'bar@kangaroo'
        self._assert_user_is_invalid(self.user)

    def test_email_cannot_contain_symbol_at_duplicates(self):
        self.user.email = 'foo@@kangaroo.com'
        self._assert_user_is_invalid(self.user)

    """
    Test name
    """

    def test_name_can_equal_100_characters(self):
        self.user.name = 'a' * 100
        self._assert_user_is_valid(self.user)

    def test_name_cannot_exceed_100_characters(self):
        self.user.name = 'a' * 101
        self._assert_user_is_invalid(self.user)

    def test_name_cannot_be_blank(self):
        self.user.name = ''
        self._assert_user_is_invalid(self.user)

    def test_name_does_not_have_to_be_unique(self):
        self.user.name = self.secondary_user.name
        self._assert_user_is_valid(self.user)

    def test_name_can_have_spaces(self):
        self.user.name = "Foo Kangaroo"
        self._assert_user_is_valid(self.user)

    def test_name_can_have_hyphens(self):
        self.user.name = "Foo-Kangaroo"
        self._assert_user_is_valid(self.user)

    def test_name_can_have_diacritics(self):
        self.user.name = """
        Á á À Â à Â â Ä ä Ã ã Å å Æ æ Ç ç Ð ð É é È è Ê ê Ë ë Í í Ì ì Î î Ï ï
        """
        self._assert_user_is_valid(self.user)

    def test_name_can_contain_non_latin_scripts(self):
        self.user.name = """
        համար التركيز елементарен 最近 საბეჭდი απλά מוסחת और เนื้อหา இப்சம்
        """
        self._assert_user_is_valid(self.user)


    def test_name_cannot_have_numbers(self):
        for digit in range(0, 10):
            self.user.name = str(digit)
            self._assert_user_is_invalid(self.user)

    def test_name_cannot_have_symbols(self):
        for symbol in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', 
        ',', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', 
        '`', '{', '|', '}', '~', '¡', '¢', '£', '¤', '¥', '¦', '§', '¨', '©', 
        '«', '¬', '®', '¯', '°', '±', '´', '¶', '·', '¸', '»', '¿', '×', '÷', 
        '\\']:
            self.user.name = symbol
            self._assert_user_is_invalid(self.user)
