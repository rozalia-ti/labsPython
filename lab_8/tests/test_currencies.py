import unittest
from unittest.mock import patch, Mock
import requests
from api import MockApi, ApplicationApi
from models.currency import Currency


class TestGetCurrencies(unittest.TestCase):

    def setUp(self):
        self.mock_xml_response = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="12.12.2024" name="Foreign Currency Market">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>91,2345</Value>
        <VunitRate>91,2345</VunitRate>
    </Valute>
    <Valute ID="R01239">
        <NumCode>978</NumCode>
        <CharCode>EUR</CharCode>
        <Nominal>1</Nominal>
        <Name>Евро</Name>
        <Value>99,1234</Value>
        <VunitRate>99,1234</VunitRate>
    </Valute>
    <Valute ID="R01035">
        <NumCode>826</NumCode>
        <CharCode>GBP</CharCode>
        <Nominal>1</Nominal>
        <Name>Фунт стерлингов</Name>
        <Value>115,5678</Value>
        <VunitRate>115,5678</VunitRate>
    </Valute>
</ValCurs>"""

    @patch('requests.get')
    def test_get_currencies_correct_return(self, mock_get):
        mock_response = Mock()
        mock_response.content = self.mock_xml_response.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api_instance = ApplicationApi()
        result = api_instance.get_currencies(['USD', 'EUR', 'GBP'])

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

        for currency in result:
            self.assertIsInstance(currency, Currency)

        usd_currency = next(c for c in result if c.char_code == 'USD')
        self.assertEqual(usd_currency.value, 91.2345)

        eur_currency = next(c for c in result if c.char_code == 'EUR')
        self.assertEqual(eur_currency.value, 99.1234)

        gbp_currency = next(c for c in result if c.char_code == 'GBP')
        self.assertEqual(gbp_currency.value, 115.5678)

    @patch('requests.get')
    def test_get_currencies_with_default_list(self, mock_get):
        extended_xml = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="12.12.2024" name="Foreign Currency Market">"""

        test_values = {
            'USD': '91,2345', 'EUR': '99,1234', 'GBP': '115,5678',
            'JPY': '0,6123', 'CNY': '12,3456', 'KZT': '0,1987',
            'CHF': '105,4321', 'CAD': '67,8901', 'AUD': '59,8765',
            'SGD': '67,1234', 'HKD': '11,6789', 'NOK': '8,5432',
            'SEK': '8,7654', 'TRY': '2,9876', 'PLN': '22,3456',
            'DKK': '13,2987', 'HUF': '0,2567', 'CZK': '3,9876',
            'RON': '20,1234', 'BGN': '50,6789', 'BRL': '18,3456',
            'INR': '1,0987', 'UAH': '2,3456', 'BYN': '28,7654',
            'AMD': '0,2345'
        }

        for i, (char_code, value) in enumerate(test_values.items()):
            extended_xml += f"""
    <Valute ID="R{i:05d}">
        <NumCode>{i}</NumCode>
        <CharCode>{char_code}</CharCode>
        <Nominal>1</Nominal>
        <Name>Test Currency</Name>
        <Value>{value}</Value>
        <VunitRate>{value}</VunitRate>
    </Valute>"""

        extended_xml += "\n</ValCurs>"

        mock_response = Mock()
        mock_response.content = extended_xml.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api_instance = ApplicationApi()
        result = api_instance.get_currencies()

        default_currencies = ApplicationApi.CURRENCY_CODES_DEFAULT
        self.assertEqual(len(result), len(default_currencies))

        result_codes = [currency.char_code for currency in result]
        for code in default_currencies:
            self.assertIn(code, result_codes)

    @patch('requests.get')
    def test_get_currencies_nonexistent_currency(self, mock_get):
        mock_response = Mock()
        mock_response.content = self.mock_xml_response.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api_instance = ApplicationApi()
        result = api_instance.get_currencies(['XXX', 'USD'])

        self.assertEqual(len(result), 3)
        char_codes = [c.char_code for c in result]
        self.assertIn('USD', char_codes)
        self.assertNotIn('XXX', char_codes)

    @patch('requests.get')
    def test_get_currencies_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Connection failed")

        api_instance = ApplicationApi()

        with self.assertRaises(ConnectionError):
            api_instance.get_currencies()

    @patch('requests.get')
    def test_get_currencies_value_error_on_invalid_xml(self, mock_get):
        mock_response = Mock()
        mock_response.content = b"Invalid XML data"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api_instance = ApplicationApi()

        with self.assertRaises(KeyError):
            api_instance.get_currencies(['USD'])

    @patch('requests.get')
    def test_get_currencies_key_error_on_missing_valute(self, mock_get):
        mock_response = Mock()
        mock_response.content = b"""<?xml version="1.0"?>
<ValCurs Date="12.12.2024">
    <NotValute>Test</NotValute>
</ValCurs>"""
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api_instance = ApplicationApi()

        with self.assertRaises(KeyError):
            api_instance.get_currencies(['USD'])

    @patch('requests.get')
    def test_get_currencies_type_error_on_invalid_rate(self, mock_get):
        invalid_xml = """<?xml version="1.0"?>
<ValCurs Date="12.12.2024">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>NOT_A_NUMBER</Value>
        <VunitRate>NOT_A_NUMBER</VunitRate>
    </Valute>
</ValCurs>"""

        mock_response = Mock()
        mock_response.content = invalid_xml.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api_instance = ApplicationApi()

        with self.assertRaises(TypeError):
            api_instance.get_currencies(['USD'])

    @patch('requests.get')
    def test_get_currencies_specific_currency_subset(self, mock_get):
        mock_response = Mock()
        mock_response.content = self.mock_xml_response.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        api_instance = ApplicationApi()
        result = api_instance.get_currencies(['EUR'])

        self.assertEqual(len(result), 3)
        char_codes = [c.char_code for c in result]
        self.assertIn('EUR', char_codes)

    def test_mock_api_get_currencies(self):
        api_instance = MockApi()
        result = api_instance.get_currencies()

        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

        for currency in result:
            self.assertIsInstance(currency, Currency)

        result_subset = api_instance.get_currencies(['USD', 'EUR'])
        self.assertEqual(len(result_subset), 25)
        char_codes = [c.char_code for c in result_subset]
        self.assertIn('USD', char_codes)
        self.assertIn('EUR', char_codes)


if __name__ == '__main__':
    unittest.main()
