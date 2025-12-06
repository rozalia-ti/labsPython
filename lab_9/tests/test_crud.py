import unittest
from unittest.mock import MagicMock, patch
from controllers.databasecontroller import DatabaseController
from controllers.currencycontroller import CurrencyController
from models.currency import Currency
from models.user import User

class TestDatabaseController(unittest.TestCase):
    """Тесты для DatabaseController"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.db = DatabaseController(":memory:")
        
        self.test_currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value="91.2345",
            nominal="1",
            rate="91.2345"
        )
    
    def test_create_and_read_currency(self):
        """Тест создания и чтения валюты"""
        result = self.db.create_currency(self.test_currency)
        self.assertTrue(result)
        
        currency = self.db.read_currency_by_char_code("USD")
        self.assertIsNotNone(currency)
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.name, "Доллар США")
    
    def test_create_duplicate_currency(self):
        """Тест создания дубликата валюты"""
        result1 = self.db.create_currency(self.test_currency)
        self.assertTrue(result1)
        
        result2 = self.db.create_currency(self.test_currency)
        self.assertFalse(result2)
    
    def test_update_currency_value(self):
        """Тест обновления курса валюты"""
        self.db.create_currency(self.test_currency)
        
        new_value = 95.1234
        result = self.db.update_currency_value("USD", new_value)
        self.assertTrue(result)
        
        currency = self.db.read_currency_by_char_code("USD")
        self.assertEqual(currency.value, str(new_value))
    
    def test_delete_currency(self):
        """Тест удаления валюты"""
        self.db.create_currency(self.test_currency)
        
        result = self.db.delete_currency("R01235")
        self.assertTrue(result)
        
        currency = self.db.read_currency_by_char_code("USD")
        self.assertIsNone(currency)
    
    def test_create_and_read_user(self):
        """Тест создания и чтения пользователя"""
        user_id = self.db.create_user("Тестовый Пользователь")
        self.assertIsNotNone(user_id)
        
        user = self.db.read_user_by_id(user_id)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Тестовый Пользователь")
    
    def test_user_currency_relationship(self):
        """Тест связи пользователь-валюта"""
        user_id = self.db.create_user("Тестовый Пользователь")
        
        self.db.create_currency(self.test_currency)
        
        result = self.db.create_user_currency(user_id, "R01235")
        self.assertTrue(result)
        
        currencies = self.db.read_user_currencies(user_id)
        self.assertEqual(len(currencies), 1)
        self.assertEqual(currencies[0].char_code, "USD")
    
    def tearDown(self):
        """Очистка после каждого теста"""
        self.db.close()

class TestCurrencyController(unittest.TestCase):
    """Тесты для CurrencyController"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.mock_db = MagicMock(spec=DatabaseController)
        self.controller = CurrencyController(self.mock_db)
    
    @patch('controllers.currencycontroller.ApplicationApi')
    def test_update_currency_from_api_success(self, MockApi):
        """Тест успешного обновления валюты из API"""
        mock_api_instance = MockApi.return_value
        mock_currency = MagicMock(spec=Currency)
        mock_currency.char_code = "USD"
        mock_currency.value = 92.3456
        mock_api_instance.get_currencies.return_value = [mock_currency]
        
        self.mock_db.update_currency_value.return_value = True
        
        result = self.controller.update_currency_from_api("USD")
        
        mock_api_instance.get_currencies.assert_called_once_with(["USD"])
        self.mock_db.update_currency_value.assert_called_once_with("USD", 92.3456)
        self.assertTrue(result)
    
    @patch('controllers.currencycontroller.ApplicationApi')
    def test_update_currency_from_api_failure(self, MockApi):
        """Тест неудачного обновления валюты из API"""
        mock_api_instance = MockApi.return_value
        mock_api_instance.get_currencies.return_value = []
        
        result = self.controller.update_currency_from_api("USD")
        
        self.assertFalse(result)
        self.mock_db.update_currency_value.assert_not_called()
    
    def test_list_currencies(self):
        """Тест получения списка валют"""
        mock_currencies = [
            MagicMock(spec=Currency),
            MagicMock(spec=Currency)
        ]
        self.mock_db.read_currencies.return_value = mock_currencies
        
        result = self.controller.list_currencies()
        
        self.assertEqual(result, mock_currencies)
        self.mock_db.read_currencies.assert_called_once()
    
    def test_delete_currency(self):
        """Тест удаления валюты"""
        self.mock_db.delete_currency.return_value = True
        
        result = self.controller.delete_currency("R01235")
        
        self.assertTrue(result)
        self.mock_db.delete_currency.assert_called_once_with("R01235")

if __name__ == '__main__':
    unittest.main()