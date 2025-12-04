#Тесты функции
import unittest
from unittest.mock import patch, Mock
from io import StringIO
import logging
from currencies import get_currencies, default_list

class TestGetCurrencies(unittest.TestCase):
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.mock_xml_response = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="12.12.2024" name="Foreign Currency Market">
    <Valute ID="R01235">
        <NumCode>840</NumCode>
        <CharCode>USD</CharCode>
        <Nominal>1</Nominal>
        <Name>Доллар США</Name>
        <Value>91,2345</Value>
    </Valute>
    <Valute ID="R01239">
        <NumCode>978</NumCode>
        <CharCode>EUR</CharCode>
        <Nominal>1</Nominal>
        <Name>Евро</Name>
        <Value>99,1234</Value>
    </Valute>
    <Valute ID="R01035">
        <NumCode>826</NumCode>
        <CharCode>GBP</CharCode>
        <Nominal>1</Nominal>
        <Name>Фунт стерлингов</Name>
        <Value>115,5678</Value>
    </Valute>
</ValCurs>"""
        
        # ожидаемый результат 
        self.expected_rates = {
            'USD': 91.2345,
            'EUR': 99.1234,
            'GBP': 115.5678
        }
    
    @patch('your_module.requests.get')
    def test_get_currencies_correct_return(self, mock_get):
        """Тест корректного возврата курсов валют"""
        mock_response = Mock()
        mock_response.content = self.mock_xml_response.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_currencies(currency_codes=['USD', 'EUR', 'GBP'])
        
        self.assertIsInstance(result, dict)
        self.assertEqual(set(result.keys()), {'USD', 'EUR', 'GBP'})
        
        for value in result.values():
            self.assertIsInstance(value, float)
        
        self.assertEqual(result['USD'], 91.2345)
        self.assertEqual(result['EUR'], 99.1234)
        self.assertEqual(result['GBP'], 115.5678)
    
    @patch('your_module.requests.get')
    def test_get_currencies_with_default_list(self, mock_get):
        """Тест с параметрами по умолчанию"""
        extended_xml = """<?xml version="1.0" encoding="windows-1251"?>
<ValCurs Date="12.12.2024" name="Foreign Currency Market">"""
        
        test_values = {
            'USD': 91.2345, 'EUR': 99.1234, 'GBP': 115.5678,
            'JPY': 0.6123, 'CNY': 12.3456, 'KZT': 0.1987,
            'CHF': 105.4321, 'CAD': 67.8901, 'AUD': 59.8765,
            'SGD': 67.1234, 'HKD': 11.6789, 'NOK': 8.5432,
            'SEK': 8.7654, 'TRY': 2.9876, 'PLN': 22.3456,
            'DKK': 13.2987, 'HUF': 0.2567, 'CZK': 3.9876,
            'RON': 20.1234, 'BGN': 50.6789, 'BRL': 18.3456,
            'INR': 1.0987, 'UAH': 2.3456, 'BYN': 28.7654,
            'AMD': 0.2345
        }
        
        for char_code, value in test_values.items():
            extended_xml += f"""
    <Valute ID="RXXXXX">
        <NumCode>000</NumCode>
        <CharCode>{char_code}</CharCode>
        <Nominal>1</Nominal>
        <Name>Test Currency</Name>
        <Value>{value}</Value>
    </Valute>"""
        
        extended_xml += "\n</ValCurs>"
        
        mock_response = Mock()
        mock_response.content = extended_xml.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_currencies()
        
        self.assertEqual(set(result.keys()), set(default_list))
        
        for value in result.values():
            self.assertIsInstance(value, float)
    
    @patch('your_module.requests.get')
    def test_get_currencies_nonexistent_currency(self, mock_get):
        """Тест поведения при несуществующей валюте"""
        mock_response = Mock()
        mock_response.content = self.mock_xml_response.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError) as context:
            get_currencies(currency_codes=['XXX'])
        
        self.assertIn("Валюта XXX отсутствует в данных", str(context.exception))
    
    def test_get_currencies_connection_error(self):
        """Тест выброса ConnectionError при проблемах с соединением"""
        with patch('your_module.requests.get') as mock_get:
            mock_get.side_effect = Exception("Connection failed")
            
            with self.assertRaises(ConnectionError):
                get_currencies()
    
    @patch('your_module.requests.get')
    def test_get_currencies_value_error_on_invalid_xml(self, mock_get):
        """Тест выброса ValueError при некорректном XML"""
        mock_response = Mock()
        mock_response.content = b"Invalid XML data"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            get_currencies(currency_codes=['USD'])
        
        self.assertIn("Некорректные данные в ответе API", str(context.exception))
    
    @patch('your_module.requests.get')
    def test_get_currencies_key_error_on_missing_valute(self, mock_get):
        """Тест выброса KeyError при отсутствии тега Valute"""
        mock_response = Mock()
        mock_response.content = b"""<?xml version="1.0"?>
<ValCurs Date="12.12.2024">
    <NotValute>Test</NotValute>
</ValCurs>"""
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError) as context:
            get_currencies(currency_codes=['USD'])
        
        self.assertIn("Ключ 'Valute' не найден", str(context.exception))
    
    @patch('your_module.requests.get')
    def test_get_currencies_type_error_on_invalid_rate(self, mock_get):
        """Тест выброса TypeError при некорректном значении курса"""
        invalid_xml = """<?xml version="1.0"?>
<ValCurs Date="12.12.2024">
    <Valute ID="R01235">
        <CharCode>USD</CharCode>
        <Value>NOT_A_NUMBER</Value>
    </Valute>
</ValCurs>"""
        
        mock_response = Mock()
        mock_response.content = invalid_xml.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        with self.assertRaises(TypeError) as context:
            get_currencies(currency_codes=['USD'])
        
        self.assertIn("Курс валюты USD имеет неверный тип", str(context.exception))
    
    @patch('your_module.requests.get')
    def test_get_currencies_specific_currency_subset(self, mock_get):
        """Тест получения подмножества валют"""
        mock_response = Mock()
        mock_response.content = self.mock_xml_response.encode('windows-1251')
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = get_currencies(currency_codes=['EUR'])
        
        self.assertEqual(len(result), 1)
        self.assertIn('EUR', result)
        self.assertIsInstance(result['EUR'], float)

    def test_get_currencies_custom_url(self):
        """Тест с использованием кастомного URL"""
        self.skipTest("Пропускаем реальный запрос к API")
        with patch('your_module.requests.get'):
            pass

if __name__ == '__main__':
    unittest.main()