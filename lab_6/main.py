import timeit
import matplotlib.pyplot as plt
import random
from collections import deque
from typing import Dict, Any, Callable, Union


def build_tree_recursive(height: int = 5, root: int = 1) -> dict:
    """рекурсивная функция для генерации непосредственно словаря дерева"""
    if height < 0:
        raise ValueError("Высота дерева не может быть отрицательной!")
    elif height == 0:
        # Базовый случай: высота 0 - возвращаем только корень
        return {
            'value': root,
            'left': None,
            'right': None
        }
    else:
        left_child = root * 2
        right_child = root + 3
        # рекурсия
        left_tree = build_tree_recursive(height - 1, left_child)
        right_tree = build_tree_recursive(height - 1, right_child)
        # возвращается словарь с измененным корнем
        return {
            'value': root,
            'left': left_tree,
            'right': right_tree
        }


def build_tree_iterative(height: int = 5, 
                 root: Union[int, float] = 1, 
                 left_branch: Callable[[Union[int, float]], Union[int, float]] = lambda x: x*2, 
                 right_branch: Callable[[Union[int, float]], Union[int, float]] = lambda x: x+3
                ) -> Dict[str, Any]:
    """
    Функция генерации бинарного дерево с использованием deque() - добавлением и удалением из очереди, а также lambda-функций для левого и правого дочерних элементов.
    """
    #если высота 0 или отрицательная - возвращаем только корень
    if height <= 0:
        return {'value': root, 'left': None, 'right': None}
    # создание корневого узла с изначальным значением (дефолт это 1)
    tree: Dict[str, Any] = {'value': root, 'left': None, 'right': None}
    # очередь для обхода в ширину: (узел, текущая высота)
    queue: deque = deque() #здесь просто создаётся пустой массив. Очередь пуста.
    queue.append((tree, 0))  # Добавляем в этот массив корень с высотой 0 и значением как у tree 
    
    while queue:
        #извлекаем нужный нам узел чтобы работать с ним, на его основе строить дочерник значения
        current_node: Dict[str, Any]
        current_height: int
        current_node, current_height = queue.popleft()
        # если текущая высота меньше максимальной, создаем потомков
        if current_height < height:
            current_value: Union[int, float] = current_node['value']
            #создаем левого потомка
            left_value: Union[int, float] = left_branch(current_value)
            left_node: Dict[str, Any] = {'value': left_value, 'left': None, 'right': None}
            current_node['left'] = left_node
            queue.append((left_node, current_height + 1))
            #создаем правого потомка
            right_value: Union[int, float] = right_branch(current_value)
            right_node: Dict[str, Any] = {'value': right_value, 'left': None, 'right': None}
            current_node['right'] = right_node
            queue.append((right_node, current_height + 1))
    return tree


def benchmark(func, data, number=100, repeat=3):
    """возвращает среднее время выполнения func на наборе data"""
    total = 0
    for n in data:
        times = timeit.repeat(lambda: func(n), number=number, repeat=repeat)
        total += min(times)
    return total / len(data)


def main():
    random.seed(42)
    test_data = list(range(3, 16))
    
    res_recursive = []
    res_iterative = []
    
    for n in test_data: 
        # рекурсивный
        time_recursive = benchmark(lambda h: build_tree_recursive(h, 1), [n], number=100, repeat=3)
        res_recursive.append(time_recursive)
        # итеративный
        time_iterative = benchmark(lambda h: build_tree_iterative(h, 1), [n], number=100, repeat=3)
        res_iterative.append(time_iterative)
    # строим график
    plt.figure(figsize=(10, 6))
    plt.plot(test_data, res_iterative, label="Итеративный", marker='o', linewidth=2, color='blue')
    plt.plot(test_data, res_recursive, label="Рекурсивный", marker='s', linewidth=2, color='green')
    plt.xlabel("Высота дерева")
    plt.ylabel("Время (сек)")
    plt.title("Сравнение методов построения деревьев")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()