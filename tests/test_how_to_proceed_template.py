import unittest
from flask import render_template

from tests.helpers import with_client, setUpApp, with_context


class TestHowToProceedTemplate(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_returning_borrower(self, client):

        html_string = render_template('howtoproceed.html',
                                      borrower_data={'borrower_name': 'Bob Smith', 'order': 'First'},
                                      conveyancer="Test Conveyancer", signed=True)

        required_string_1 = "Your information"
        self.assertIn(required_string_1, html_string)

        required_string_2 = "Sign your mortgage deed by agreeing Land Registry's terms of use for this service"
        self.assertIn(required_string_2, html_string)

        required_string_3 = "Continue"
        self.assertIn(required_string_3, html_string)
