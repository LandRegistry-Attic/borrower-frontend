from tests.helpers import with_client, setUpApp, with_context
import unittest
from lxml.html import document_fromstring
import mock
import requests

class TestHealth(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_start_route(self, client):
        res = client.get('/health')
        html = document_fromstring(res.get_data())

        self.assertEqual(res.status_code, 200)

        header = ''.join(html.xpath('//header//a/text()'))
        self.assertTrue('GOV.UK' in header)

    @with_context
    @with_client
    def test_assets_path_correct(self, client):
        res = client.get('/health')
        html = document_fromstring(res.get_data())

        self.assertEqual(res.status_code, 200)
        assetPaths = html.xpath('//link/@href')
        for path in assetPaths:
            self.assertTrue('/assets/', '/static/' in path)

    """
    def my_super_awesome_test(self, mock_get, mock_patch):
        mock_get.status_code = 500

        resp = self.app.get(path_to_my_method)

        self.assertEqual(resp, status.HTTP_200_OK)
    """

    @mock.patch('application.health.views.DeedApiInterface')
    def test_service_check_route(self, mock_get):

        response = self.app.get(self.DEED_API_BASE_HOST + '/health/service-check',
                                headers={"Content-Type": "application/json"})

        #res = client.get('/health/service-check')
        #self.assertEqual(res.status_code, 200)

        #resDict = json.loads(res.text)

        self.assertEqual(True, False)

        #
