from flask import session
from tests.helpers import with_client, setUpApp, with_context, MockDeedClass
import unittest
from application.deed.searchdeed.views import validate_dob, search_deed_search
from application.borrower.views import confirm_network_agreement
from datetime import date
from unittest.mock import patch, Mock
from flask.ext.api import status


class TestAgreementNaa(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @patch('application.service.deed_api.interface.DeedApiInterface.send_naa')
    @patch('application.borrower.views.render_template')
    @patch('application.borrower.views.request')
    def test_confirm_network_agreement_get(self, mock_request, mock_render, mock_sign):
        mock_request.method = "GET"
        mock_sign.status_code = 200
        confirm_network_agreement()
        mock_render.assert_called_with('howtoproceed.html')

    @with_context
    @patch('application.borrower.views.redirect')
    @patch('application.borrower.views.request')
    def test_confirmed_network_agreement_no_request_form(self, mock_request, mock_redirect):
        mock_request.method = "POST"
        confirm_network_agreement()
        mock_redirect.assert_called_with('/how-to-proceed', code=307)

    @with_context
    @patch('application.borrower.views.redirect')
    @patch('application.borrower.views.request')
    def test_confirmed_network_agreement_declined(self, mock_request, mock_redirect):
        mock_request.method = "POST"
        mock_request.form = {'validate': 'True', 'decline-naa': 'Decline'}
        confirm_network_agreement()
        self.assertEqual(session['agreement_naa'],  "declined")
        mock_redirect.assert_called_with('/how-to-proceed', code=307)

    @with_context
    @patch('application.borrower.views.make_deed_api_client', autospec=False)
    @patch('application.borrower.views.redirect')
    @patch('application.borrower.views.request')
    def test_confirmed_network_agreement_accepted(self, mock_request, mock_redirect, mock_sign):
        mock_request.method = "POST"
        mock_request.form = {'validate': 'True', 'accept-naa': 'Accept'}
        session['borrower_id'] = 00000
        mock_sign.return_value = MockDeedClass()
        confirm_network_agreement()
        self.assertEqual(session['agreement_naa'],  "accepted")
        mock_redirect.assert_called_with('/mortgage-deed', code=302)

    @with_context
    @patch('application.deed.searchdeed.views.redirect')
    def test_search_deed_search_deed_token(self, mock_redirect):
        search_deed_search()
        mock_redirect.assert_called_with('/session-ended', code=302)

    @with_context
    @patch('application.deed.searchdeed.views.redirect')
    def test_search_deed_search_no_agreement(self, mock_redirect):
        session['deed_token'] = 'test'
        search_deed_search()
        mock_redirect.assert_called_with('/how-to-proceed', code=307)

        session['agreement_naa'] = 'declined'
        search_deed_search()
        mock_redirect.assert_called_with('/how-to-proceed', code=307)

    @with_context
    @patch('application.deed.searchdeed.views.redirect')
    @patch('application.deed.searchdeed.views.do_search_deed_search')
    def test_search_deed_search_success(self, mock_search, mock_redirect):
        session['deed_token'] = 'test'
        session['agreement_naa'] = 'accepted'
        mock_search.return_value = 'ok'
        self.assertEqual(search_deed_search(), ('ok', 200))


class TestSearchDeed(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    @patch('application.akuma.service.Akuma.do_check')
    def test_search_deed_post(self, client, mock_akuma):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'
            sess['agreement_naa'] = 'accepted'
            sess['borrower_token'] = 'AABB1232'

        mock_akuma.return_value = {
            "result": "A",
            "id": "2b9115b2-d956-11e5-942f-08002719cd16"
        }

        res = client.get('/mortgage-deed')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    @patch('application.akuma.service.Akuma.do_check')
    def test_search_deed_post_invalid_reference(self, client, mock_akuma):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'
            sess['agreement_naa'] = 'accepted'
            sess['borrower_token'] = 'AABB1232'

        mock_akuma.return_value = {
            "result": "A",
            "id": "2b9115b2-d956-11e5-942f-08002719cd16"
        }

        res = client.get('/mortgage-deed')

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_validate_borrower(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'

        res = client.post('/date-of-birth', data={'borrower_token': 'vvAAA',
                                                  'dob-day': '01',
                                                  'dob-month': '10',
                                                  'dob-year': '1976',
                                                  'dob': '01/11/1975',
                                                  'validate': 'True'})
        self.assertEqual(session['borrower_token'], 'VVAAA')
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
            sess['borrower_token'] = 'A2C5G6'

        res = client.post('/enter-authentication-code', data={'auth_code': 'AAA123'})

        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    def test_show_confirming_deed_page_check(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'
            sess['borrower_token'] = 'A2C5V6'

        res = client.post('/signing-mortgage-deed', data={'auth_code': 'AAA123'})

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
