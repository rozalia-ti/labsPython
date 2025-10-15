# код для разработки и проверки разных значений в терминале
from main import gen_bin_tree
height = int(input("Введите значение высоты:"))
root = int(input("Введите значение корня:"))
tree = gen_bin_tree(height, root)

def print_tree_advanced(tree_dict, prefix="", is_left=True):
    """функиця для форматирования словаря бинарного дерева в читабельный формат"""
    if tree_dict is None:
        return
 
    print_tree_advanced(tree_dict.get('right'), prefix + ("│   " if is_left else "    "), False)
    print(prefix + ("└── " if is_left else "┌── ") + str(tree_dict['value']))
    print_tree_advanced(tree_dict.get('left'), prefix + ("    " if is_left else "│   "), True)

print(tree)
print('\n')
print_tree_advanced(tree) #печать дерева в горизонтальном формате