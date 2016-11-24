import unittest
from application.deed.searchdeed.views import check_all_signed, no_of_borrowers


class TestBorrowerUtils(unittest.TestCase):

    def test_check_all_signed(self):
        # check_all_signed returns true if all borrowers have a key called signature
        fake_deed_data = {"deed": {"borrowers": [{"signature": 1}, {"signature": 2}]}}
        self.assertEqual(check_all_signed(fake_deed_data), True)
        fake_deed_data = {"deed": {"borrowers": [{"dummy": 1}, {"signature": 2}]}}
        self.assertEqual(check_all_signed(fake_deed_data), False)

    def test_no_of_borrowers(self):
        fake_deed_data = {"deed": {"borrowers": [{"a": 1}, {"b": 2}]}}
        self.assertEqual(no_of_borrowers(fake_deed_data), 2)
        fake_deed_data = None
        self.assertEqual(no_of_borrowers(fake_deed_data), 0)
