import sys
from functools import wraps


def logger(func=None, *, handle=sys.stdout):
    def wrapper(func):
        @wraps(func)
        def logger_stdout(*args, **kwargs):
            print()
            func(*args, **kwargs)
            
        return logger_stdout
    return wrapper


@logger()
def x(y=None):
    print(y)

x(y=1)
