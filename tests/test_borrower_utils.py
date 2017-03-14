import unittest
from application.deed.searchdeed.views import check_all_signed, no_of_borrowers
from application.borrower.views import get_ordered_borrowers, inflect_ordered_borrowers
from application.deed.searchdeed.borrower_utils import get_signed_in_borrower


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

    def test_get_ordered_borrowers(self):
        # Relies on deed_data['deed']['borrowers'] and session token
        fake_deed_data = []
        session_borrower_token = 'ABC12345'

        # If deed_data is empty, assert that it returns an empty dict
        self.assertEqual(get_ordered_borrowers(fake_deed_data, session_borrower_token), [])

        # If deed_data is not empty
        fake_deed_data = {'deed': {'borrowers': [
            {'forename': 'Adam', 'middle_name': 'Chnages', 'surname': 'Smith', 'token': 'ABB00001'},
            {'forename': 'Chloe', 'surname': 'Bob', 'token': 'ABB00000', 'signature': 'A fake date'},
            {'forename': 'Ann', 'surname': 'Smith', 'token': 'ABC12345'}]}}

        response = get_ordered_borrowers(fake_deed_data, session_borrower_token)

        # Check that the ordering has been changed and that the signed in borrower is at the top of the dict
        # or at index 0, in other words
        self.assertEqual('Ann Smith' in response[0].values(), True)

        # Check that a middle name is found if specified
        self.assertTrue('Adam Chnages Smith' in response[1].values())

        # Check if middle name is not inside of a borrowers data, if a middle name is not specified
        self.assertTrue('Chloe Bob' in response[2].values())

        # Check if the returned dict has 'signed' = False for a borrower who has not signed yet, or else True
        self.assertEqual(response[1]['signed'], False)
        self.assertEqual(response[2]['signed'], True)

    def test_inflect_ordered_borrowers(self):

        # Create an empty dict and determine if the function returns nothing if the initial
        # check on the contents of the dict fails
        fake_ordered_borrower_data = []
        self.assertEqual(inflect_ordered_borrowers(fake_ordered_borrower_data), [])

        # Create the fake dict of borrower data - taken from above
        fake_ordered_borrower_data = [{'borrower_name': 'Ann Smith', 'order': 0, 'signed': False},
                                      {'borrower_name': 'Adam Chnages Smith', 'order': 1, 'signed': False},
                                      {'borrower_name': 'Chloe Bob', 'order': 2, 'signed': True}]

        # Check that the method inflects the ordered numbers in an ordinal way, so that the
        # How to proceed page can display the borrowers in the correct order
        # Note that the function also capitalises the word - Adam
        response = inflect_ordered_borrowers(fake_ordered_borrower_data)

        self.assertEqual(response[0]['order'], 'First')
        self.assertEqual(response[1]['order'], 'Second')
        self.assertEqual(response[2]['order'], 'Third')

    def test_get_signed_in_borrower(self):
        deed_data = {'deed': {'borrowers': [
            {'forename': 'Anthony', 'middle_name': 'Stewart', 'surname': 'Head', 'token': 'ABB00002'},
            {'forename': 'Charisma', 'surname': 'Carpenter', 'token': 'ABB00003', 'signature': 'A fake date'},
            {'forename': 'Alyson', 'surname': 'Hannigan', 'token': 'ABB00004'}]}}

        self.assertEqual(get_signed_in_borrower(deed_data, 'ABB00002'), 'Anthony Stewart Head')
        self.assertEqual(get_signed_in_borrower(deed_data, 'ABB00003'), 'Charisma Carpenter')
        self.assertEqual(get_signed_in_borrower(deed_data, 'ABB00004'), 'Alyson Hannigan')
