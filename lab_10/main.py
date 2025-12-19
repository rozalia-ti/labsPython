import time
import math

# Настройки теста
FUNC = math.cos
A = 0
B = math.pi
N_ITER = 100000

# 1. Базовая реализация
print("1. Базовый Python")
from base_integration import integrate
start = time.time()
res = integrate(FUNC, A, B, n_iter=N_ITER)
base_time = time.time() - start
print(f"Время: {base_time:.4f}с")

# 2. Потоки
print("\n2. Потоки")
from threaded_integration import integrate_threaded
start = time.time()
res = integrate_threaded(FUNC, A, B, n_jobs=4, n_iter=N_ITER)
thread_time = time.time() - start
print(f"Время: {thread_time:.4f}с")

# 3. Процессы
print("\n3. Процессы")
if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    
    from process_integration import integrate_multiprocess
    start = time.time()
    res = integrate_multiprocess(FUNC, A, B, n_jobs=4, n_iter=N_ITER)
    process_time = time.time() - start
    print(f"Время: {process_time:.4f}с")

# 4. Cython
print("\n4. Cython")
import sys
sys.path.insert(0, 'cython_integration')
import integrate_cy  # type: ignore

start = time.time()
res = integrate_cy.integrate_cython_optimized(A, B, N_ITER)
cy_time = time.time() - start
print(f"Время: {cy_time:.4f}с")

print("\nВыводы:")
print("1. Базовый Python: время выполнения - " + str(base_time) + "с")
print("2. Потоки: время выполнения - " + str(thread_time) + "с")
print("3. Процессы: время выполнения - " + str(process_time) + "с")
print("4. Cython: время выполнения - " + str(cy_time) + "с")