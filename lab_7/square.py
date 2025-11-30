from logger import logger
import sys 
from io import StringIO
import logging

stream = StringIO()
log = logging.getLogger("L1")
@logger(handle = log)
def solve_quadratic(a, b, c):
    D = b**2 - 4 * a * c;
    return D

# a = int(input())
# b = int(input())
# c = int(input())
solve_quadratic(4, 2, 1)