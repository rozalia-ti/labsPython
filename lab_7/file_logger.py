import logging


file_logger = logging.getLogger("currency_file")
def logger(func=None, *, handle=file_logger):
    if func == None:
        # print('it seems to me func = None type!')
        return lambda f: logger(f, handle=handle) #else func = None!
    handle.setLevel(logging.INFO)
    file_handler = logging.FileHandler('currency_file.txt')
    file_logger.addHandler(file_handler)
    res = func()
    file_logger.info(res)
    

@logger(handle=file_logger)
def ssdum():
    return 'stroka';

