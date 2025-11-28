import sys


def logger(func=None, *, handle=sys.stdout):
    def wrapper(*args, **kwargs):
        match handle:
            case sys.stdout:
                handle.write(f"before function launch\n")
                res = func(*args, **kwargs)
                handle.write(f"result = {res} \n")
                handle.write('after function launch\n')
                return res
    return wrapper

# @logger      
# def current(*args, **kwargs):
#     return (f"args:{args} \n kwargs: {kwargs} \n");
# current(1, 'i wanna be ypur slave', True, omega = 'PSG', name = 'Roza', age = 18)

@logger
def sum(a, b):
    return a + b;
sum(3, 7)

