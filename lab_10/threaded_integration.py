import concurrent.futures as ftres
from functools import partial
from typing import Callable
from base_integration import integrate
import time


def integrate_threaded(f: Callable[[float], float], a: float, b: float, *, n_jobs: int = 2, n_iter: int = 100000) -> float:
    executor = ftres.ThreadPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter//n_jobs)
    
    step = (b - a) / n_jobs
    futures = []
    
    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        print(f"Работник {i}, границы: {left:.6f}, {right:.6f}")
        futures.append(spawn(left, right))
    
    results = []
    for future in ftres.as_completed(futures):
        results.append(future.result())
    
    executor.shutdown(wait=True)
    return sum(results)


def benchmark_threaded():
    """Замер производительности для разного количества потоков"""
    import math
    
    test_cases = [
        (math.cos, 0, math.pi, "cos(x) от 0 до π"),
        (lambda x: x**2, 0, 2, "x² от 0 до 2"),
    ]
    
    n_jobs_list = [1, 2, 4, 6, 8]
    
    for func, a, b, description in test_cases:
        print(f"\nТест: {description}")
        print("-" * 40)
        
        for n_jobs in n_jobs_list:
            start_time = time.time()
            result = integrate_threaded(func, a, b, n_jobs=n_jobs, n_iter=1000000)
            elapsed = time.time() - start_time
            
            print(f"Потоков: {n_jobs:2d}, "
                  f"Время: {elapsed:.4f} сек, "
                  f"Результат: {result:.6f}")

if __name__ == "__main__":
    benchmark_threaded()