import unittest
from flask import render_template

from tests.helpers import with_client, setUpApp, with_context


class TestHowToProceedTemplate(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_returning_borrower(self, client):
        # Signed = True
        html_string = render_template('howtoproceed.html', conveyancer="Test Conveyancer", signed=True)

        required_string_1 = "View your mortgage deed"
        self.assertIn(required_string_1, html_string)

        required_string_2 = "View your mortgage deed by agreeing Land Registry's terms and conditions for this service."
        self.assertIn(required_string_2, html_string)

        required_string_3 = "Continue"
        self.assertIn(required_string_3, html_string)

        # Signed = False
        html_string = render_template('howtoproceed.html', conveyancer="Test Conveyancer", signed=False)

        required_string_1 = "Agree to the Land Registry's terms and conditions for this service"
        self.assertIn(required_string_1, html_string)

        required_string_2 = "Read your mortgage deed carefully"
        self.assertIn(required_string_2, html_string)

        required_string_3 = "Confirm your mortgage deed is correct"
        self.assertIn(required_string_3, html_string)

        required_string_4 = "Sign your mortgage deed"
        self.assertIn(required_string_4, html_string)

        required_string_5 = "Next"
        self.assertIn(required_string_5, html_string)
