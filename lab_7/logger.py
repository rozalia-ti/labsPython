import sys
from io import StringIO
import logging
import functools
import inspect

stream = StringIO()
log = logging.getLogger("L1")
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
        
        def except_console_write(func, handle):
            try: 
                res = func(*args, **kwargs)
                handle.write(f"Функция {func.__name__} завершила свою работу с результатом: {res} \n")
                return res
            except Exception as e:
                handle.write(f"!!!ФУНКИЦЯ {func.__name__} ЗАВЕРШИЛА СВОЮ РАБОТУ С ВОТ ЭТОЙ ОШИБКОЙ : {type(e).__name__}. ВОТ ТЕКСТ ЭТОЙ ОШИБКИ: {str(e)} \n")
                raise
            
        def just_console_write(handle = sys.stdout):
            params = get_sign_params()
            handle.write(f"Функция {func.__name__} начала работу с параметрами {params}. \n")
            res = except_console_write(func, handle = handle)
            return res
         
        if handle is sys.stdout: #i dont use match/case because it disturb to have an access to stream variable inside a case-item 
            just_console_write(handle)
        elif isinstance(handle, StringIO):
            params = get_sign_params()
            handle.write(f"Функция {func.__name__} начала работу с параметрами {params}. \n")
            try: 
                res = func(*args, **kwargs)
                handle.write(f"Функция {func.__name__} завершила свою работу с результатом: {res} \n")
                content = handle.getvalue()
                print(content)
                return res
            except Exception as e:
                handle.write(f"!!!ФУНКЦИЯ {func.__name__} ЗАВЕРШИЛА СВОЮ РАБОТУ С ВОТ ЭТОЙ ОШИБКОЙ: {type(e).__name__}. ВОТ ТЕКСТ ЭТОЙ ОШИБКИ: {str(e)} \n")
                content = stream.getvalue()
                print(content)
                raise
            
        elif isinstance(handle, logging.Logger): #check that handle is Logger class
            params = get_sign_params()
            log.setLevel(logging.INFO)
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            log.addHandler(console_handler)
            try:
                log.info(f"Функция {func.__name__} начала работу с параметрами {params}.")
                res = func(*args, **kwargs)
                log.info(f"Функция {func.__name__} завершила свою работу с результатом: {res} \n")
                return res
            except Exception as e:
                log.error(f"!!!ФУНКЦИЯ {func.__name__} ЗАВЕРШИЛА СВОЮ РАБОТУ С ВОТ ЭТОЙ ОШИБКОЙ: {type(e).__name__}. ВОТ ТЕКСТ ЭТОЙ ОШИБКИ: {str(e)} \n")
                raise
        else: 
            print("Не был распознан вариант логирования. По умолчанию выбран 'sys.stdout' \n")
            just_console_write()
            return               
    return wrapper










