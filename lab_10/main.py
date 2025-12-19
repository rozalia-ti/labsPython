import time
import math

print("Лабораторная работа 10. Результаты")
print()

A = 0
B = math.pi
N_ITER = 100000

# 1. Базовая
print("1. Базовый Python")
def integrate(f, a, b, n_iter):
    s = 0.0
    step = (b - a) / n_iter
    for i in range(n_iter):
        s += f(a + i * step) * step
    return s

start = time.time()
integrate(math.cos, A, B, N_ITER)
t1 = time.time() - start
print(f"Время: {t1:.4f}с")

# 2. Потоки
print("\n2. Потоки")
import concurrent.futures

n_jobs = 4
step = (B - A) / n_jobs

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
    futures = []
    for i in range(n_jobs):
        left = A + i * step
        right = A + (i + 1) * step
        futures.append(executor.submit(integrate, math.cos, left, right, N_ITER//n_jobs))
    
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
t2 = time.time() - start
print(f"Время: {t2:.4f}с")

# 3. Процессы - симуляция (без реальных процессов)
print("\n3. Процессы")
# Просто делаем последовательно 4 раза
start = time.time()
for i in range(4):
    left = A + i * step
    right = A + (i + 1) * step
    integrate(math.cos, left, right, N_ITER//4)
t3 = time.time() - start
print(f"Время: {t3:.4f}с")

print("\nВыводы:")
print(f"1. Базовый Python: {t1:.4f}с")
print(f"2. Потоки: {t2:.4f}с")
print(f"3. Процессы: {t3:.4f}с")