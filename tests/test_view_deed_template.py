import unittest
from flask import render_template

from tests.helpers import with_client, setUpApp, with_context


class TestViewDeedTemplate(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_returning_borrower(self, client):
        html_string = render_template('viewdeed.html',
                                      deed_data={"deed": {"lender": "Lender", "charge_clause": ""}},
                                      signed=True, conveyancer='Test Land Registry Devices')

        required_string_1 = "Is this correct?"
        self.assertIn(required_string_1, html_string)

        required_string_2 = "You may need to contact Test Land Registry Devices. " \
                            "If corrections to your mortgage deed need to be made."
        self.assertIn(required_string_2, html_string)
