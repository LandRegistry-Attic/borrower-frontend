import unittest
from flask import render_template

from bs4 import BeautifulSoup

from tests.helpers import with_client, setUpApp, with_context
from tests.complete_deed_dict import complete_deed_dict


class TestViewDeedTemplate(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    @with_context
    @with_client
    def test_returning_borrower(self, client):
        # Signed = True
        html_string = render_template('viewdeed.html',
                                      deed_data={"deed": {"lender": "Lender", "charge_clause": ""}},
                                      signed=True, conveyancer='Test Land Registry Devices')

        required_string_1 = "Is this correct?"
        self.assertIn(required_string_1, html_string)

        required_string_2 = "You may need to contact Test Land Registry Devices " \
                            "if corrections to your mortgage deed need to be made."
        self.assertIn(required_string_2, html_string)

        required_string_2 = "Finish"
        self.assertIn(required_string_2, html_string)

        # Signed = False
        html_string = render_template('viewdeed.html',
                                      deed_data={"deed": {"lender": "Lender", "charge_clause": ""}},
                                      signed=False, conveyancer='Test Land Registry Devices')

        required_string_1 = "Receiving your authentication code"
        self.assertIn(required_string_1, html_string)

        required_string_2 = "Send my code"
        self.assertIn(required_string_2, html_string)

    def remove_whitespace(self, some_text):
        return some_text.replace(' ', '')

    def get_html_string(self, template, deed_dict, signed, conveyancer):
        html_string = render_template(template,
                                      deed_data=deed_dict,
                                      signed=signed, conveyancer=conveyancer)
        no_carriage_returns = html_string.replace("\n", "")
        return self.remove_whitespace(no_carriage_returns)

    @with_context
    @with_client
    def test_title_rendered(self, client):
        html_string = self.get_html_string('viewdeed.html', complete_deed_dict, True, 'Test Land Registry Devices')
        self.assertIn('WYK722599', html_string)

    @with_context
    @with_client
    def test_borrower_names_rendered(self, client):
        html_string = self.get_html_string('viewdeed.html', complete_deed_dict, True, 'Test Land Registry Devices')
        self.assertIn('JuliaHannahNorthin', html_string)
        self.assertIn('MrDavidAlanJewers', html_string)

    @with_context
    @with_client
    def test_address_rendered(self, client):
        html_string = self.get_html_string('viewdeed.html', complete_deed_dict, True, 'Test Land Registry Devices')
        soup = BeautifulSoup(html_string, 'html.parser')
        html_text = soup.get_text()
        self.assertIn('5TheDrive,ThisTown,ThisCounty,PL44TH', html_text)

    @with_context
    @with_client
    def test_lender_rendered(self, client):
        html_string = self.get_html_string('viewdeed.html', complete_deed_dict, True, 'Test Land Registry Devices')
        soup = BeautifulSoup(html_string, 'html.parser')
        html_text = soup.get_text()
        self.assertIn('COVENTRYBUILDINGSOCIETYEconomicHousePOBox9,HighStreetCoventryCV15QN', html_text)

    @with_context
    @with_client
    def test_date_of_mortgage_offer_rendered(self, client):
        html_string = self.get_html_string('viewdeed.html', complete_deed_dict, True, 'Test Land Registry Devices')
        soup = BeautifulSoup(html_string, 'html.parser')
        html_text = soup.get_text()
        self.assertIn('DateofMortgageOfferadatestring', html_text)

    @with_context
    @with_client
    def test_charging_clause_rendered(self, client):
        html_string = self.get_html_string('viewdeed.html', complete_deed_dict, True, 'Test Land Registry Devices')
        soup = BeautifulSoup(html_string, 'html.parser')
        html_text = soup.get_text()
        self.assertIn('Chargingclause', html_text)
        self.assertIn('Theborrower,withfulltitleguarantee,chargestothelenderthepropertybywayoflegalmortgage', html_text)
        self.assertIn('withpaymentofallmoneysecuredbythecharge.', html_text)

    @with_context
    @with_client
    def test_lender_reference_rendered(self, client):
        html_string = self.get_html_string('viewdeed.html', complete_deed_dict, True, 'Test Land Registry Devices')
        soup = BeautifulSoup(html_string, 'html.parser')
        html_text = soup.get_text()
        self.assertIn('Coventryreference:123', html_text)
