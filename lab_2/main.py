def userInput() -> int:
    """функция ввода пользователя"""
    target = int(input("Загаданное число:" ))
    min = int(input("Нижняя граница:" ))
    max = int(input("Верхняя граница:" ))
    return target, min, max

def toArrayFromInput(min: int, max: int) -> list[int]:
    """функция преобразования в массив из входных данных. Нужна чтобы не писать два раза в инпуте и без него."""
    arr = []
    for i in range(min, max + 1):
        arr.append(i)
        i += 1
    arr.sort()
    return arr


def guess(target: int, arr: list[int])-> list[int] | int:
    """реализация алгоритма бинарного поиска"""
    min = arr[0]
    length = len(arr)
    max = arr[length - 1]
    mid = 0
    counter = 0

    while min <= max:
        counter += 1
        mid = (max + min) // 2
        if arr[mid] < target:
            min = mid + 1
        elif arr[mid] > target:
            max = mid - 1
        else:
            #искомое число
            return arr[mid], counter
        

def mainFunc(target: int, min: int, max: int)-> list[int]:
    """итоговая функция"""
    arr = toArrayFromInput(min, max)
    guessedNum, iterationNum = guess(target, arr)
    # здесь возможен вывод, если программа должна выводить значения (не тест)
    # print("Угаданное число:", guessedNum,  "\nКоличество итераций:", iterationNum)
    return [guessedNum, iterationNum]
   

# юзер френдли ввод и сам запуск функции. Оно нам не надо, потому что мы запускаем только тесты.

# target_value, min_value, max_value = userInput()
# mainFunc(target_value, min_value, max_value)

