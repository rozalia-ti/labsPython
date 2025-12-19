# cython: language_level=3
"""
Cython реализации функции интегрирования
"""

# Импорты из стандартной математической библиотеки C
from libc.math cimport cos
import cython


# ============================================================================
# Версия 1: Базовая Cython
# ============================================================================
def integrate_cython_basic(double a, double b, int n_iter):
    """
    Базовая Cython реализация.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += cos(a + i * step) * step
    
    return acc


# ============================================================================
# Версия 2: Оптимизированная
# ============================================================================
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython_optimized(double a, double b, int n_iter):
    """
    Оптимизированная Cython версия.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += cos(a + i * step) * step
    
    return acc


# ============================================================================
# Версия 3: Без GIL
# ============================================================================
@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython_nogil(double a, double b, int n_iter):
    """
    Cython реализация без GIL.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    with nogil:
        for i in range(n_iter):
            acc += cos(a + i * step) * step
    
    return acc