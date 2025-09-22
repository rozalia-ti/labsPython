# тестирнуемая функция в файле tests.py. Возвращает словарь.
def gen_bin_tree(height: int = 5, root: int = 1) -> dict:
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
        left_tree = gen_bin_tree(height - 1, left_child)
        right_tree = gen_bin_tree(height - 1, right_child)
        # возвращается словарь с измененным корнем
        return {
            'value': root,
            'left': left_tree,
            'right': right_tree
        }








