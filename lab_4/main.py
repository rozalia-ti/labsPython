import timeit
import matplotlib.pyplot as plt
import random
from functools import lru_cache


def fact_recursive(n: int) -> int:
    """Рекурсивный факториал"""
    if n == 0:
        return 1
    return n * fact_recursive(n - 1)


@lru_cache(maxsize=None)
def fact_recursive_cached(n: int) -> int:
    """Рекурсивный факториал с кешированием"""
    if n == 0:
        return 1
    return n * fact_recursive_cached(n - 1)


def fact_iterative(n: int) -> int:
    """Итеративный факториал"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


@lru_cache(maxsize=None)
def fact_iterative_cached(n: int) -> int:
    """Итеративный факториал с кешированием"""
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res


def benchmark(func, data, number=1, repeat=5):
    """Возвращает среднее время выполнения func на наборе data"""
    total = 0
    for n in data:
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)
    return total / len(data)


def main():
    random.seed(42)
    test_data = list(range(20, 150, 10))

    res_recursive = []
    res_iterative = []
    res_recursive_cached = []
    res_iterative_cached = []

    for n in test_data:
        res_recursive.append(benchmark(fact_recursive, [n], number=10000, repeat=5))
        res_iterative.append(benchmark(fact_iterative, [n], number=10000, repeat=5))
        res_recursive_cached.append(benchmark(fact_recursive_cached, [n], number=10000, repeat=5))
        res_iterative_cached.append(benchmark(fact_iterative_cached, [n], number=10000, repeat=5))

    plt.figure(figsize=(12, 5))
#первый график
    plt.subplot(1, 2, 1)
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_iterative_cached, label="Итеративный с кешированием", color='red')
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение с итеративным кешированием")
    plt.legend()
#второй график
    plt.subplot(1, 2, 2)
    plt.plot(test_data, res_iterative, label="Итеративный")
    plt.plot(test_data, res_recursive, label="Рекурсивный")
    plt.plot(test_data, res_recursive_cached, label="Рекурсивный с кешированием", color='green')
    plt.xlabel("n")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение с рекурсивным кешированием")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()