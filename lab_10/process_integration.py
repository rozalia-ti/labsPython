import concurrent.futures as ftres
from functools import partial
from typing import Callable
from base_integration import integrate
import time


def integrate_multiprocess(f: Callable[[float], float], a: float, b: float, *, n_jobs: int = 2, n_iter: int = 100000) -> float:
    executor = ftres.ProcessPoolExecutor(max_workers=n_jobs)
    spawn = partial(executor.submit, integrate, f, n_iter=n_iter//n_jobs)
    step = (b - a) / n_jobs
    futures = []
    for i in range(n_jobs):
        left = a + i * step
        right = a + (i + 1) * step
        futures.append(spawn(left, right))
    
    results = []
    for future in ftres.as_completed(futures):
        results.append(future.result())
    
    executor.shutdown(wait=True)
    return sum(results)


def benchmark_processes():
    """Замер производительности для разного количества процессов"""
    import math
    
    n_jobs_list = [1, 2, 4, 6, 8]
    n_iter = 1000000
    
    print("\nСравнение производительности процессов")
    print("=" * 50)
    
    for n_jobs in n_jobs_list:
        start_time = time.time()
        result = integrate_multiprocess(
            math.cos, 0, math.pi, 
            n_jobs=n_jobs, 
            n_iter=n_iter
        )
        elapsed = time.time() - start_time
        
        speedup = 1.0 if n_jobs == 1 else None
        if n_jobs > 1:
            start_single = time.time()
            integrate_multiprocess(math.cos, 0, math.pi, n_jobs=1, n_iter=n_iter)
            single_time = time.time() - start_single
            speedup = single_time / elapsed
        
        print(f"Процессов: {n_jobs:2d}, "
              f"Время: {elapsed:.4f} сек, "
              f"Ускорение: {speedup:.2f}x, "
              f"Результат: {result:.6f}")


def compare_threads_vs_processes():
    """Сравнение потоков и процессов"""
    import math
    from threaded_integration import integrate_threaded
    
    n_iter = 500000
    
    print("\nСравнение потоков и процессов")
    print("=" * 50)
    
    methods = [
        ("Потоки", integrate_threaded),
        ("Процессы", integrate_multiprocess),
    ]
    
    for name, method in methods:
        print(f"\n{name}:")
        for n_workers in [2, 4]:
            start_time = time.time()
            result = method(math.cos, 0, math.pi, 
                           n_jobs=n_workers, 
                           n_iter=n_iter)
            elapsed = time.time() - start_time
            print(f"  Работников: {n_workers}, Время: {elapsed:.4f} сек")


if __name__ == "__main__":
    benchmark_processes()
    compare_threads_vs_processes()