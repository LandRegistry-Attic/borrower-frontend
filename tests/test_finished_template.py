import unittest
from flask import render_template

from tests.helpers import with_client, setUpApp, with_context
from application.deed.searchdeed.views import check_all_signed, no_of_borrowers


class TestFinishedTemplate(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_all_signed(self, client):
        deed_data = {"deed": {"borrowers": [{"signature": 1}, {"signature": 2}]}}
        html_string = render_template('finished.html', all_signed=check_all_signed(deed_data))
        required_string_1 = "The conveyancer will be notified so that they can continue to do the legal work " \
            "needed for your mortgage"
        self.assertIn(required_string_1, html_string)

    @with_context
    @with_client
    def test_one_borrower(self, client):
        deed_data = {"deed": {"borrowers": [{"signature": 1}]}}
        html_string = render_template('finished.html', all_signed=check_all_signed(deed_data))
        required_string_1 = "The conveyancer will be notified so that they can continue to do the legal work " \
                            "needed for your mortgage"
        self.assertIn(required_string_1, html_string)

    # Todo - last test for one or more unsigned borrower