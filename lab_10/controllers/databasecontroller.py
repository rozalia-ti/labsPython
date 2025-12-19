import sqlite3
from typing import List, Optional
from models.currency import Currency
from models.user import User

class DatabaseController:
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn = None
        self._init_database()
    
    def _init_database(self):
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency (
                id TEXT PRIMARY KEY,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                value REAL,
                nominal INTEGER,
                rate REAL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_currency (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id TEXT NOT NULL,
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(currency_id) REFERENCES currency(id),
                UNIQUE(user_id, currency_id)
            )
        """)
        
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    # User CRUD
    def create_user(self, name: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO user (name) VALUES (?)", (name,))
        self.conn.commit()
        return cursor.lastrowid
    
    def read_users(self) -> List[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM user")
        return [User(id=row[0], name=row[1]) for row in cursor.fetchall()]
    
    def read_user_by_id(self, user_id: int) -> Optional[User]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name FROM user WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return User(id=row[0], name=row[1]) if row else None
    
    # Currency CRUD
    def create_currency(self, currency: Currency) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO currency 
            (id, num_code, char_code, name, value, nominal, rate) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            currency.id, currency.num_code, currency.char_code,
            currency.name, currency.value, currency.nominal, currency.rate
        ))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def read_currencies(self) -> List[Currency]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, num_code, char_code, name, value, nominal, rate FROM currency")
        rows = cursor.fetchall()
        
        currencies = []
        for row in rows:
            currencies.append(Currency(
                id=row[0], num_code=row[1], char_code=row[2],
                name=row[3], value=str(row[4]), nominal=str(row[5]),
                rate=str(row[6])
            ))
        return currencies
    
    def update_currency_value(self, char_code: str, value: float) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE currency SET value = ? WHERE char_code = ?", (value, char_code))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_currency(self, currency_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM currency WHERE id = ?", (currency_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    # User-Currency relations
    def create_user_currency(self, user_id: int, currency_id: str) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO user_currency (user_id, currency_id) VALUES (?, ?)", 
                      (user_id, currency_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def read_user_currencies(self, user_id: int) -> List[Currency]:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.id, c.num_code, c.char_code, c.name, c.value, c.nominal, c.rate
            FROM currency c
            INNER JOIN user_currency uc ON c.id = uc.currency_id
            WHERE uc.user_id = ?
        """, (user_id,))
        
        rows = cursor.fetchall()
        currencies = []
        for row in rows:
            currencies.append(Currency(
                id=row[0], num_code=row[1], char_code=row[2],
                name=row[3], value=str(row[4]), nominal=str(row[5]),
                rate=str(row[6])
            ))
        return currencies
    
    def populate_initial_data(self, mock_api):
        users = mock_api.get_users()
        for user in users:
            self.create_user(user.name)
        
        currencies = mock_api.get_currencies()
        for currency in currencies:
            self.create_currency(currency)
        
        user_currencies = mock_api.get_user_currencies()
        for uc in user_currencies:
            self.create_user_currency(uc.user_id, uc.id)