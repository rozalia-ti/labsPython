import requests
from bs4 import BeautifulSoup
from typing import Dict, List

default_list = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'KZT', 'CHF', 'CAD', 'AUD', 
            'SGD', 'HKD', 'NOK', 'SEK', 'TRY', 'PLN', 'DKK', 'HUF', 'CZK', 
            'RON', 'BGN', 'BRL', 'INR', 'UAH', 'BYN', 'AMD']
def get_currencies(currency_codes: List[str] = default_list, url: str = "https://www.cbr.ru/scripts/XML_daily.asp") -> Dict[str, float]:
    """
    Получает курсы валют с API ЦБ РФ
    
    Args:
        currency_codes: Список кодов валют для получения (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ
    
    Returns:
        Словарь с курсами валют вида {"USD": 93.25, "EUR": 101.7}
    
    Raises:
        ConnectionError: API недоступен
        ValueError: Некорректные данные
        KeyError: Нет ключа "Valute" или валюта отсутствует в данных
        TypeError: Курс валюты имеет неверный тип
    """
    # Запрос к API
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API недоступен: {e}")

    # Парсинг XML
    try:
        soup = BeautifulSoup(response.content, 'xml')
        valute_elements = soup.find_all('Valute')
        
        if not valute_elements:
            raise KeyError("Ключ 'Valute' не найден в ответе API")
        
        # Извлекаем все валюты в словарь
        all_valutes: Dict[str, float] = {}
        for valute in valute_elements:
            char_code_elem = valute.find('CharCode')
            value_elem = valute.find('Value')
            
            if char_code_elem is None or value_elem is None:
                continue
                
            char_code = char_code_elem.text
            value_text = value_elem.text
            
            # Проверяем тип курса валюты
            try:
                rate_value = float(value_text.replace(',', '.'))
            except (ValueError, TypeError):
                raise TypeError(f"Курс валюты {char_code} имеет неверный тип: {value_text}")
            
            all_valutes[char_code] = rate_value
        
        # Проверяем наличие запрошенных валют и формируем результат
        result: Dict[str, float] = {}
        for code in currency_codes:
            if code not in all_valutes:
                raise KeyError(f"Валюта {code} отсутствует в данных")
            result[code] = all_valutes[code]
        
        return result
        
    except Exception as e:
        if isinstance(e, (KeyError, TypeError)):
            raise e
        raise ValueError(f"Некорректные данные в ответе API: {e}")


# Примеры использования
if __name__ == "__main__":
    try:
        # Получаем 20+ валют
        rates = get_currencies() #заданы стандартные параметры
        # print(rates)
    
    except ConnectionError as e:
        print(f"Ошибка соединения: {e}")
    except ValueError as e:
        print(f"Ошибка данных: {e}")
    except KeyError as e:
        print(f"Ошибка ключа: {e}")
    except TypeError as e:
        print(f"Ошибка типа: {e}")
