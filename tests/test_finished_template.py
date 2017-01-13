import unittest
from flask import render_template

from tests.helpers import with_client, setUpApp, with_context


class TestFinishedTemplate(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_all_signed(self, client):
        html_string = render_template('finished.html', all_signed=True, conveyancer='The conveyancer')
        required_string_1 = "The conveyancer will be notified so that they can continue to do the legal work " \
                            "needed for your mortgage"
        self.assertIn(required_string_1, html_string)

    @with_context
    @with_client
    def test_with_unsigned_borrower(self, client):
        html_string = render_template('finished.html', all_signed=False, conveyancer='the conveyancer')
        required_string_1 = "As you are borrowing money with other people, they will also need to sign the " \
                            "mortgage deed"
        self.assertIn(required_string_1, html_string)
        required_string_2 = "Once all borrowers have signed the mortgage deed, the conveyancer will be notified " \
                            "so that they can continue to do the legal work needed for your mortgage"
        self.assertIn(required_string_2, html_string)

    @with_context
    @with_client
    def test_with_returning_borrower(self, client):
        html_string = render_template('finished.html', returning_borrower=True, all_signed=False, conveyancer='the conveyancer')
        required_string_1 = "Thank you for viewing your mortgage deed, you have successfully signed out"
        self.assertIn(required_string_1, html_string)

        required_string_2 = "Didn't want to sign out? Sign in here"
        self.assertIn(required_string_2, html_string)

        required_string_3 = "Return to GOV.UK"
        self.assertIn(required_string_3, html_string)

