# Демонстрационный пример (квадратное уравнение).
from io import StringIO
import logging

def logger(func):
    log = logging.getLogger(__name__)
    log.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    log.addHandler(console_handler)
    
    def wrapper(a_1, b_1, c_1):
        try:
            res = func(a_1, b_1, c_1)
            
            if res > 0:
                log.info(f'INFO: Уравнение имеет 2 действительных корня. D = {res}')
            elif a_1 == 0 and b_1 == 0:
                log.critical(f'CRITICAL: Коэффикиценты a = b = 0. Уравнение не имеет решений.')
            elif a_1 == 0:
                log.critical(f'CRITICAL: Уравнение не является квадратным. Коэффициент а = 0')
            elif res == 0:
                log.info(f'INFO: Уравнение имеет один корень, D = 0.')
            elif res < 0:
                log.warning(f'WARNING: Уравнение не имеет действительных корней, D < 0.')
            else:
                log.warning(f'WARNING: Неизвестная ошибка')
                
        except TypeError as e:
            log.error(f'ERROR: Некорректный тип результата: {type(res).__name__}, значение: {res}')
            
        except Exception as e:
            log.error(f'ERROR: Произошла неизвестная ошибка: {str(e)}')
            
    return wrapper

@logger
def solve_quadratic(a, b, c):
    D = b**2 - 4 * a * c;    
    return D

# solve_quadratic(2, 6, 3) # 2 корня
# solve_quadratic(0, 0, 34) № a = b = 0. Решений нет.
solve_quadratic(0, -3, -1)
