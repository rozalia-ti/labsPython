from collections import deque
from typing import Dict, Any, Optional, Callable, Union

def gen_bin_tree(height: int = 5, 
                 root: Union[int, float] = 1, 
                 left_branch: Callable[[Union[int, float]], Union[int, float]] = lambda x: x*2, 
                 right_branch: Callable[[Union[int, float]], Union[int, float]] = lambda x: x+3
                ) -> Dict[str, Any]:
    """
    Функция генерации бинарного дерево с испольщованием deque() - добавлением и удалением из очереди, а также lambda-функций для левого и правого дочерних элементов.
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
