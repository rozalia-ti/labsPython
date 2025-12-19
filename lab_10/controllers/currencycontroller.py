from typing import List, Optional
from models.currency import Currency
from controllers.databasecontroller import DatabaseController
from api import ApplicationApi

class CurrencyController:
    
    def __init__(self, db_controller: DatabaseController):
        self.db = db_controller
        self.api = ApplicationApi()
    
    def list_currencies(self) -> List[Currency]:
        return self.db.read_currencies()
    
    def update_currency_from_api(self, char_code: str) -> bool:
        try:
            currencies = self.api.get_currencies([char_code])
            if currencies:
                return self.db.update_currency_value(char_code, currencies[0].value)
            return False
        except Exception:
            return False
    
    def sync_currencies_from_api(self) -> int:
        try:
            api_currencies = self.api.get_currencies()
            added_count = 0
            for currency in api_currencies:
                if self.db.create_currency(currency):
                    added_count += 1
            return added_count
        except Exception:
            return 0
    
    def get_currency_by_code(self, char_code: str) -> Optional[Currency]:
        currencies = self.db.read_currencies()
        for currency in currencies:
            if currency.char_code == char_code:
                return currency
        return None