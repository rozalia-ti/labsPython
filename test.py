from main import two_sum
import unittest

class TestMySolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(two_sum([0, 6.3], 6.3), [0, 1]) #здесь вводить значения списка и таргета
    
if __name__ ==  '__main__':
    unittest.main()
#P.S. я сделала только один тест потому что не вижу смысла тестировать что-то ещё, например, действительно ли входными параметрами являются целочисленные значения, потому что этот параметр у нас и проверяет тест assertEqual, потому что в функцию two_sum я добавила условие которое предотвращает иные случаи. 