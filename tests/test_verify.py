import unittest
from flask import url_for
from urllib.parse import urlparse
from tests.helpers import with_client, with_context, setUpApp
from werkzeug.datastructures import Headers


class TestVerify(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    # Test that the start URL will redirect to borrower-reference page without the Verify env set
    def test_verify_start(self, client):
        res = client.get(url_for('borrower_landing.start'), follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, url_for('searchdeed.search_deed_main'))
        self.assertEqual(res.status_code, 307)

    @with_context
    @with_client
    # Test that if there is a previous session (deed_token is present) that you go to identity_verified page
    def test_previous_session(self, client):
        with client.session_transaction() as sess:
            sess['deed_token'] = '063604'
        res = client.get(url_for('borrower_landing.identity_verified'))
        self.assertEqual(res.status_code, 200)

    @with_context
    @with_client
    # Test that if there is no previous session (deed_token is not present) that you get a 401.
    # This will get picked up by the interceptor
    def test_no_previous_session(self, client):
        res = client.get(url_for('borrower_landing.identity_verified'))
        self.assertEqual(res.status_code, 401)

    @with_context
    @with_client
    # Test that a valid Pid from verify will validate and go to the identity_verified page
    def test_verify_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'), headers=Headers([('Pid', '111111')]),
                          follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, url_for('borrower_landing.identity_verified'))
        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    # Test that an invalid Pid (Broken at this stage of the flow) from verify will validate and go to the
    # server-error page
    def test_verify_broken_pid_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'), headers=Headers([('Pid', '111112')]),
                          follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, '/server-error')
        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    # Test when verify tells us 'no-match' we go to a no match page
    def test_verify_no_match_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'),
                          headers=Headers([('Verify-response-status', 'no-match')]), follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, url_for('borrower_landing.verify_no_match'))
        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    # Test when verify tells us 'NoAuthnContext' we go to a verify-error page
    def test_verify_no_authn_context_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'),
                          headers=Headers([('Verify-response-status', 'NoAuthnContext')]), follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, url_for('borrower_landing.verify_error'))
        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    # Test when verify tells us 'AuthnFailed' we go to a verify-error page
    def test_verify_no_authn_failed_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'),
                          headers=Headers([('Verify-response-status', 'AuthnFailed')]), follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, url_for('borrower_landing.verify_error'))
        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    # Test when verify tells us 'AuthnFailed' we go to a verify-error page
    def test_verify_requester_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'),
                          headers=Headers([('Verify-response-status', 'Requester')]), follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, url_for('borrower_landing.verify_error'))
        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    # Test when verify tells us 'Some Other Response' we go to a verify-error page
    def test_verify_other_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'),
                          headers=Headers([('Verify-response-status', 'unknown')]), follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, url_for('borrower_landing.verify_error'))
        self.assertEqual(res.status_code, 302)

    @with_context
    @with_client
    # Test when someone posts nothing to the service
    def test_verify_no_pid_or_response(self, client):
        res = client.post(url_for('borrower_landing.verify_identity'), follow_redirects=False)
        self.assertEqual(urlparse(res.location).path, '/server-error')
        self.assertEqual(res.status_code, 302)
