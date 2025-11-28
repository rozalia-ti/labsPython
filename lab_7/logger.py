import sys

#поток вывода в консоль
def logger(func=None, *, handle=sys.stdout):
    def wrapper():
        handle.write(f"before function launch\n")
        func()
        handle.write('after function launch\n')
    return wrapper

# @logger(handle)      
# def current(handle):
#     handle.write("24\n");
# current(handle = sys.stdout)
