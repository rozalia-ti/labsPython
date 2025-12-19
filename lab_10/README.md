# Лабораторная работа №10: Методы оптимизации вычислений
## Выполнила Тихонова Роза 501455 Р3122.

## **Цель работы**
Исследование методов оптимизации вычисления кода с использованием:
- Потоков (`ThreadPoolExecutor`)
- Процессов (`ProcessPoolExecutor`)
- Cython
- Отключения GIL (Global Interpreter Lock)

На примере функции численного интегрирования методом прямоугольников.
### Базовая реализация (base_integration.py)
``` def integrate(f: Callable[[float], float], 
              a: float, 
              b: float, 
              *, 
              n_iter: int = 100000) -> float: 
```

### Оптимизация потоками (threaded_integration.py)
```
def integrate_threaded(f: Callable[[float], float],
                      a: float,
                      b: float,
                      *,
                      n_jobs: int = 2,
                      n_iter: int = 100000) -> float:
```
###  Оптимизация процессами (process_integration.py)
```
def integrate_multiprocess(f: Callable[[float], float],
                          a: float,
                          b: float,
                          *,
                          n_jobs: int = 2,
                          n_iter: int = 100000) -> float:
    """Вычисление интеграла с использованием ProcessPoolExecutor."""
```
### Cython оптимизация (cython_integration/integrate_cy.pyx)
```
@cython.boundscheck(False)
@cython.wraparound(False)
def integrate_cython_optimized(double a, double b, int n_iter):
```

### Тестирование
```
# Настройки теста
FUNC = math.cos
A = 0
B = math.pi
N_ITER = 100000

# Тестирование всех методов
print("1. Базовый Python")
# ... измерение времени

print("2. Потоки")
# ... измерение времени

print("3. Процессы")
# ... измерение времени

print("4. Cython")
# ... измерение времени
```
- Потоки в Python не ускоряют CPU-задачи из-за GIL

- Процессы обеспечивают ускорение за счет параллельного выполнения

- Cython дает наибольшее ускорение за счет компиляции в C код

- Отключение GIL в Cython позволяет использовать многопоточность

## Запуск
**Компиляция**
```
cd cython_integration
python setup.py build_ext --inplace
cd .. 
```
**Основной запуск**

```
py main.py
```