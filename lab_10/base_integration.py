
import math
from typing import Callable


def integrate(f: Callable[[float], float], a: float, b: float,  *,  n_iter: int = 100000) -> float:
   # n_iter это число квадратов на которое мы разбиваем
    if n_iter <= 0:
        raise ValueError("n_iter должен быть положительным числом")
    if b <= a:
        raise ValueError("b должен быть больше a")
    acc = 0.0 # аккумулятор, к которому юудут суммироваться значения площадейм прямоугоьнков
    step = (b - a) / n_iter # один прямоугольник
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def test_basic_functionality():
    """Быстрая проверка работы функции"""
    # Тест с косинусом
    result_cos = integrate(math.cos, 0, math.pi / 2, n_iter=10000)
    print(f"∫cos(x)dx от 0 до π/2 ≈ {result_cos:.6f}")
    print(f"Ожидаемое значение: 1.0, разница: {abs(result_cos - 1.0):.6f}")
    
    # Тест с квадратичной функцией
    result_square = integrate(lambda x: x**2, 0, 2, n_iter=10000)
    print(f"∫x²dx от 0 до 2 ≈ {result_square:.6f}")
    print(f"Ожидаемое значение: 8/3 ≈ 2.666667, разница: {abs(result_square - 8/3):.6f}")


if __name__ == "__main__":
    test_basic_functionality()