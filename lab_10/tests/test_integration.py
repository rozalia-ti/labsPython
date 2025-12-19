"""
Тесты для всех реализаций интегрирования
"""
import unittest
import math
import sys
import os

# Добавляем родительскую директорию в путь
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from base_integration import integrate


class TestIntegrationBase(unittest.TestCase):
    """Тесты базовой реализации"""
    
    def test_cosine_integral(self):
        """Интеграл косинуса от 0 до pi/2 должен быть 1"""
        result = integrate(math.cos, 0, math.pi/2, n_iter=10000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)
    
    def test_sine_integral(self):
        """Интеграл синуса от 0 до pi должен быть 2"""
        result = integrate(math.sin, 0, math.pi, n_iter=10000)
        self.assertAlmostEqual(result, 2.0, delta=0.001)
    
    def test_polynomial_integral(self):
        """Интеграл x² от 0 до 2 должен быть 8/3"""
        result = integrate(lambda x: x**2, 0, 2, n_iter=10000)
        self.assertAlmostEqual(result, 8/3, delta=0.001)
    
    def test_linear_function(self):
        """Интеграл x от 0 до 1 должен быть 0.5"""
        result = integrate(lambda x: x, 0, 1, n_iter=1000)
        self.assertAlmostEqual(result, 0.5, delta=0.001)
    
    def test_negative_boundaries(self):
        """Работа с отрицательными границами"""
        result = integrate(lambda x: x**2, -1, 1, n_iter=10000)
        self.assertAlmostEqual(result, 2/3, delta=0.001)
    
    def test_invalid_iterations(self):
        """Проверка на недопустимые значения n_iter"""
        with self.assertRaises(ValueError):
            integrate(math.cos, 0, 1, n_iter=0)
        with self.assertRaises(ValueError):
            integrate(math.cos, 0, 1, n_iter=-100)
    
    def test_invalid_boundaries(self):
        """Проверка на некорректные границы"""
        with self.assertRaises(ValueError):
            integrate(math.cos, 5, 1, n_iter=1000)


# Добавьте тесты для других реализаций аналогично
class TestIntegrationThreaded(unittest.TestCase):
    """Тесты для потоковой реализации"""
    
    def setUp(self):
        from threaded_integration import integrate_threaded
        self.integrate_func = integrate_threaded
    
    def test_basic_functionality(self):
        """Базовая функциональность потоков"""
        result = self.integrate_func(math.cos, 0, math.pi/2, 
                                    n_jobs=2, n_iter=10000)
        self.assertAlmostEqual(result, 1.0, delta=0.001)
    
    def test_different_worker_counts(self):
        """Работа с разным количеством потоков"""
        for n_jobs in [1, 2, 4]:
            result = self.integrate_func(lambda x: x, 0, 1,
                                        n_jobs=n_jobs, n_iter=10000)
            self.assertAlmostEqual(result, 0.5, delta=0.001)


def run_doctests():
    """Запуск doctest из базовой реализации"""
    import doctest
    from base_integration import integrate
    
    print("Запуск doctest...")
    result = doctest.testmod()
    print(f"Doctest пройден: {result.attempted} тестов, {result.failed} ошибок")


if __name__ == "__main__":
    # Запуск doctest
    run_doctests()
    
    # Запуск unittest
    print("\nЗапуск unittest...")
    unittest.main(verbosity=2)