from abc import ABC, abstractmethod
from models.currency import Currency
from models.user import User
from models.user_currency import UserCurrency
from typing import Optional
import requests
from bs4 import BeautifulSoup

class Api(ABC):
    @abstractmethod
    def get_currencies(self, currency_codes: Optional[list[str]] = None) -> list[Currency]:
        pass

    @abstractmethod
    def get_users(self) -> list[User]:
        pass

    @abstractmethod
    def get_user_currencies(self) -> list[UserCurrency]:
        pass

class MockApi(Api):
    def get_currencies(self, currency_codes: Optional[list[str]] = None) -> list[Currency]:
        return [
            Currency("1", '100', 'USD', '1', 'Доллар США', '76.9708', "0.5"),
            Currency("2", '101', 'EUR', '1', 'Евро', '89.9011', "0.5"),
            Currency("3", '102', 'GBP', '1', 'Фунт стерлингов', '102.6098', "0.5"),
            Currency("4", '103', 'JPY', '1', 'Японская иена', '49.585', "0.5"),
            Currency("5", '104', 'CNY', '1', 'Китайский юань', '10.8487', "0.5"),
        ]

    def get_users(self) -> list[User]:
        return [
            User(1, "Бред Питт"),
            User(2, "Самовар Самоваров"),
            User(3, "Миллионер Миллиардерович"),
            User(4, "Роза Тихонова"),
            User(5, "Петр Скалкин"),
        ]

    def get_user_currencies(self) -> list[UserCurrency]:
        return [
            UserCurrency("1", 4),
            UserCurrency("2", 4),
            UserCurrency("3", 4),
            UserCurrency("1", 1),
            UserCurrency("2", 1),
        ]

class ApplicationApi(Api):
    CURRENCY_CODES_DEFAULT = ['USD', 'EUR', 'GBP', 'JPY', 'CNY']

    def get_currencies(self, currency_codes: Optional[list[str]] = None) -> list[Currency]:
        currency_codes = currency_codes or self.CURRENCY_CODES_DEFAULT

        try:
            response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp", timeout=10)
            response.raise_for_status()
        except:
            return MockApi().get_currencies(currency_codes)

        try:
            soup = BeautifulSoup(response.content, 'xml')
            valute_elements = soup.find_all('Valute')
            
            result = []
            for valute in valute_elements:
                char_code_elem = valute.find('CharCode')
                if not char_code_elem:
                    continue
                    
                char_code = char_code_elem.text
                if char_code not in currency_codes:
                    continue
                
                result.append(Currency(
                    id=valute.get('ID'),
                    num_code=valute.find('NumCode').text,
                    char_code=char_code,
                    nominal=valute.find('Nominal').text,
                    name=valute.find('Name').text,
                    value=valute.find('Value').text,
                    rate=valute.find('VunitRate').text
                ))
            
            return result if result else MockApi().get_currencies(currency_codes)
        except:
            return MockApi().get_currencies(currency_codes)

    def get_users(self) -> list[User]:
        return MockApi().get_users()

    def get_user_currencies(self) -> list[UserCurrency]:
        return MockApi().get_user_currencies()