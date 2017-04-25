from tests.helpers import setUpApp
import unittest
from application.deed.searchdeed import address_utils


class TestFormatAddress(unittest.TestCase):
    def setUp(self):
        setUpApp(self)

    def test_format_address(self):
        address = address_utils.format_address_string("103 street name, the town, the city,PL5 9ZZ")
        self.assertEqual(address, ["103 street name", "the town", "the city", "PL5 9ZZ"])

    def test_format_address_with_comma_after_house_number(self):
        address = address_utils.format_address_string("103,street name, the town, the city,PL5 9ZZ")
        self.assertEqual(address, ["103 street name", "the town", "the city", "PL5 9ZZ"])

    def test_format_address_with_whitespace(self):
        address = address_utils.format_address_string("103 street name , the town, the city , PL5 9ZZ ")
        self.assertEqual(address, ["103 street name", "the town", "the city", "PL5 9ZZ"])

    def test_format_address_with_post_code_in_wrong_place(self):
        address = address_utils.format_address_string("103 street name , the town, PL5 9ZZ ,the city")
        self.assertEqual(address, ["103 street name", "the town", "the city", "PL5 9ZZ"])

    def test_format_address_lowercase_postcode(self):
        address = address_utils.format_address_string("103 street name , the town, the city, pl6 9zz")
        self.assertEqual(address, ["103 street name", "the town", "the city", "PL6 9ZZ"])

    def test_format_combined(self):
        address = address_utils.format_address_string("103, street name , the town , the city , pl6 9zz ")
        self.assertEqual(address, ["103 street name", "the town", "the city", "PL6 9ZZ"])

    def test_address_with_no_commas(self):
        address = address_utils.format_address_string("999 Fake Road Leicester Leicestershire LE3 0SA")
        self.assertEqual(address, ["999 Fake Road Leicester Leicestershire", "LE3 0SA"])

    def test_address_with_no_comma_before_postcode(self):
        address = address_utils.format_address_string("999 Fake Road, Leicester, Leicestershire le3 0sa")
        self.assertEqual(address, ["999 Fake Road", "Leicester", "Leicestershire", "LE3 0SA"])

    def test_address_with_no_comma_before_postcode2(self):
        address = address_utils.format_address_string("999b Fake Road, Leicester, Leicestershire le3 0sa")
        self.assertEqual(address, ["999b Fake Road", "Leicester", "Leicestershire", "LE3 0SA"])

    def test_address_with_no_comma_before_postcode3(self):
        address = address_utils.format_address_string("Dunroamin, 999 Fake Road, Leicester, Leicestershire LE3 0SA")
        self.assertEqual(address, ["Dunroamin", "999 Fake Road", "Leicester", "Leicestershire", "LE3 0SA"])

    def test_address_with_no_comma_before_postcode4(self):
        address = address_utils.format_address_string("Dunroamin, 999 Fake Road, Leicester le3 0sa, Leicestershire")
        self.assertEqual(address, ["Dunroamin", "999 Fake Road", "Leicester", "Leicestershire", "LE3 0SA"])
