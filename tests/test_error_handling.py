"""
UnitTests around the Application Error Handling.
"""


import mock
import unittest

from bs4 import BeautifulSoup
from flask import json

from application import manager


app = manager.app


class TestErrorHandling(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_server_error_page(self):
        expected = 'We are unable to process your request at this time. This was not due to any mistake on your part,' \
                   ' but because the service encountered technical issues.'

        with app.app_context():
            with app.test_request_context():
                response = self.client.get('/server-error')
                soup = BeautifulSoup(response.data)
                for para in soup.find_all('p'):
                    if expected in para.text:
                        break
                else:
                    self.assertTrue(False)

    def test_page_not_found(self):
        with app.app_context():
            with app.test_request_context():
                response = self.client.get('/page-not-found')
                expected = 'We could not find the page you requested. This could be because the address was mistyped, '\
                           'or a link you followed was pointing at a page that no longer exists.'
                soup = BeautifulSoup(response.data)
                for para in soup.find_all('p'):
                    print(repr(para.text))
                    if expected in para.text:
                        break
                else:
                    self.assertTrue(False)

    @mock.patch('application.deed.searchdeed.views.redirect')
    def test_server_error_json(self, mock_flask_redirect):
        def div_by_zero(*args, **kw):
            1/0
        mock_flask_redirect.side_effect = div_by_zero
        with app.app_context():
            with app.test_request_context():
                response = self.client.get('mortgage-deed',
                                           headers={'accept': 'application/json'})
                expected = {"redirect": "/server-error?error=True", "error": True}
                self.assertEqual(expected, json.loads(response.data))

    @mock.patch('application.deed.searchdeed.views.redirect')
    def test_server_error_html(self, mock_flask_redirect):
        def div_by_zero(*args, **kw):
            1/0
        mock_flask_redirect.side_effect = div_by_zero
        with app.app_context():
            with app.test_request_context():
                response = self.client.get('/mortgage-deed')
                expected = 'We are unable to process your request at this time.'
                soup = BeautifulSoup(response.data)
                for para in soup.find_all('p'):
                    if expected in para.text:
                        break
                else:
                    self.assertTrue(False)

    def test_page_not_found_json(self):
        with app.app_context():
            with app.test_request_context():
                response = self.client.get('/foo',
                                           headers={'accept': 'application/json'})
                expected = {"redirect": "/page-not-found?error=True", "error": True}
                self.assertEqual(expected, json.loads(response.data))

    def test_page_not_found_html(self):
        with app.app_context():
            with app.test_request_context():
                response = self.client.get('/foo')
                expected = 'We could not find the page you requested'
                soup = BeautifulSoup(response.data)
                for para in soup.find_all('p'):
                    if expected in para.text:
                        break
                else:
                    self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
