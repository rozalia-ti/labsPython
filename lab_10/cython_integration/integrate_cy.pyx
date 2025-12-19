# cython: language_level=3
"""
Cython реализации функции интегрирования
"""

# Импорты из C библиотек
from libc.math cimport cos, sin
import cython
from cython.parallel import parallel, prange


# Базовая Cython (без оптимизаций)
def integrate_cython_basic(double a, double b, int n_iter, func_name="cos"):
    """
    Базовая Cython реализация.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    
    if func_name == "cos":
        for i in range(n_iter):
            x = a + i * step
            acc += cos(x) * step
    elif func_name == "sin":
        for i in range(n_iter):
            x = a + i * step
            acc += sin(x) * step
    else:
        # Используем Python функцию
        import math
        py_func = getattr(math, func_name)
        for i in range(n_iter):
            x = a + i * step
            acc += py_func(x) * step
    
    return acc


#  С оптимизациями (no boundscheck, no wraparound)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)  # Быстрое деление без проверок
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


# Без GIL и с параллелизацией (nogil)

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def integrate_cython_nogil(double a, double b, int n_iter, int n_threads=1):
    """
    Cython реализация без GIL с параллелизацией.
    
    Параметры:
    ----------
    a, b : double
        Границы интегрирования.
    n_iter : int
        Количество итераций.
    n_threads : int
        Количество потоков для prange.
    """
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double local_sum
    
    if n_threads == 1:
        # Последовательная версия без GIL
        with nogil:
            for i in range(n_iter):
                acc += cos(a + i * step) * step
    else:
        # Параллельная версия
        cdef double[:] partial_sums = [0.0] * n_threads
        
        with nogil, parallel(num_threads=n_threads):
            for i in prange(n_iter, schedule='static'):
                # Каждый поток считает свою частичную сумму
                partial_sums[cython.parallel.threadid()] += cos(a + i * step) * step
        
        # Суммируем частичные суммы
        with nogil:
            for i in range(n_threads):
                acc += partial_sums[i]
    
    return acc


# С использованием typed memoryviews

def integrate_cython_memoryview(double a, double b, int n_iter):
    """
    Версия с typed memoryviews для потенциальной интеграции с NumPy.
    """
    cdef double[:] x_values
    import numpy as np
    
    # Создаем массив значений x
    x_values = np.linspace(a, b, n_iter, endpoint=False)
    
    cdef double acc = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    
    for i in range(n_iter):
        acc += cos(x_values[i]) * step
    
    return acc