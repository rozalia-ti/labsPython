#файловый логгер
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
# from logger import logger
import sys
from io import StringIO
import logging
import inspect
import functools


default_list = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'KZT', 'CHF', 'CAD', 'AUD', 
            'SGD', 'HKD', 'NOK', 'SEK', 'TRY', 'PLN', 'DKK', 'HUF', 'CZK', 
            'RON', 'BGN', 'BRL', 'INR', 'UAH', 'BYN', 'AMD']

file_logger = logging.getLogger("currency_file")

def logger(func=None, *, handle=sys.stdout):
    if func == None:
        # print('it seems to me func = None type!')
        return lambda f: logger(f, handle=handle) #else func = None!
    @functools.wraps(func) #we need to save original naming of functions. 
    def wrapper(*args, **kwargs):
        def get_sign_params():
            signature = inspect.signature(func) 
            args_together = signature.bind(*args, **kwargs)
            args_together.apply_defaults()
            return args_together
                
        if isinstance(handle, logging.Logger): #check that handle is Logger class
            params = get_sign_params()
            handle.setLevel(logging.INFO)
            file_handler = logging.FileHandler('currency_file.txt')
            file_logger.addHandler(file_handler)
            try: 
                file_logger.info(f"function {func.__name__} started working with params {params}.")
                res = func()
                file_logger.info(f"Function {func.__name__} finished working with result: {res} \n \n")
            except Exception as e:
                file_logger.error(f"!!!FUNCTION {func.__name__} FINISHED WORKING WITH ERROR {type(e).__name__}. THERE IS A TEXT OF THIS ERROR {str(e)}")
                raise
        else: 
            print("Не был распознан вариант логирования. По умолчанию выбран 'sys.stdout' \n")
            return               
    return wrapper

    
@logger(handle=file_logger)
def get_currencies(currency_codes: List[str] = default_list, url: str = "https://www.cbr.ru/scripts/XML_daily.asp") -> Dict[str, float]:
    # API request
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API недоступен: {e}")
    #parse XML
    try:
        soup = BeautifulSoup(response.content, 'xml')
        valute_elements = soup.find_all('Valute')
        if not valute_elements:
            raise KeyError("Ключ 'Valute' не найден в ответе API")
        #go to dict
        all_valutes: Dict[str, float] = {}
        for valute in valute_elements:
            char_code_elem = valute.find('CharCode')
            value_elem = valute.find('Value')
            if char_code_elem is None or value_elem is None:
                continue
            char_code = char_code_elem.text
            value_text = value_elem.text
            #check type course
            try:
                rate_value = float(value_text.replace(',', '.'))
            except (ValueError, TypeError):
                raise TypeError(f"Курс валюты {char_code} имеет неверный тип: {value_text}")
            all_valutes[char_code] = rate_value
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
if __name__ == "__main__":
    try:
        rates = get_currencies()  # заданы стандартные параметры
        # print(rates) #print result

    except ConnectionError as e:
        print(f"Ошибка соединения: API недоступен {e}")
        raise  # Все равно поднимаем исключение, но после вывода
    except ValueError as e:
        print(f"Ошибка данных: Некорректный JSON {e}")
        raise
    except KeyError as e:
        print(f"Ошибка ключа: Нет ключа “Valute” или валюта отсутствует в данных{e}")
        raise
    except TypeError as e:
        print(f"Ошибка типа: Курс валюты имеет неверный тип	 {e}")
        raise

