from tests.helpers import with_client, setUpApp, with_context
import unittest
from application.deed.searchdeed.views import validate_dob
from datetime import date


class TestSearchDeed(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_search_deed_post(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.get('/mortgage-deed')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_search_deed_post_invalid_reference(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.get('/mortgage-deed')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_validate_borrower(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.post('/date-of-birth', data={'borrower_token': '38',
                                                  'dob-day': '01',
                                                  'dob-month': '10',
                                                  'dob-year': '1976',
                                                  'dob': '01/11/1975',
                                                  'validate': 'True'})

        self.assertEqual(res.status_code, 307)

    @with_context
    @with_client
    def test_sign_my_mortgage_landing(self, client):
        res = client.get('/')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_finish_page(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'
            sess['borrower_token'] = '38'
        res = client.post('/finished')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_how_to_proceed_page(self, client):
        res = client.post('/how-to-proceed')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_borrower_reference_page(self, client):
        res = client.get('/borrower-reference')

        self.assertEqual(res.status_code, 200)

    @with_context
    def test_validate_dob_future(self):
        form = {
            "dob-day": "01",
            "dob-month": "01",
            "dob-year": date.today().year + 1
        }
        dobResult = validate_dob(form)
        self.assertEqual(dobResult, "Please enter a valid date of birth")

    @with_context
    def test_validate_dob(self):
        form = {
            "dob-day": "01",
            "dob-month": "01",
            "dob-year": date.today().year - 1
        }
        dobResult = validate_dob(form)
        self.assertEqual(dobResult, None)

    @with_context
    @with_client
    def test_request_auth_code(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.get('/enter-authentication-code')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_authenticate_code(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'
            sess['borrower_token'] = 'A2C5v6'

        res = client.post('/enter-authentication-code', data={'auth_code': 'AAA123'})

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_show_confirming_deed_page_check(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'
            sess['borrower_token'] = 'A2C5v6'

        res = client.post('/confirming-mortgage-deed', data={'auth_code': 'AAA123'})

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_verify_auth_code(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.post('/verify-auth-code', data={'auth_code': 'AAA123'})
        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_verify_auth_code_no_js(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.post('/verify-auth-code-no-js', data={'auth_code': 'AAA123'})

        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    def test_verify_auth_code_no_js_with_missing_authcode(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.post('/verify-auth-code-no-js')

        self.assertEqual(res.status_code, 400)

    @with_context
    @with_client
    def test_confirm_mortgage_is_signed(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.get('/confirm-mortgage-is-signed')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_naa_page_shown(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.get('/confirm-naa')

        self.assertEqual(res.status_code, 200)
