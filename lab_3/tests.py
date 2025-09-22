from main import gen_bin_tree
import unittest

class Test(unittest.TestCase):
    
    def test_otrits_high(self):
        """провальный тест с отрицательной высотой дерева. На этот случай предусмотрена ошибка в коде функции"""
        result = gen_bin_tree(-1, 4)
        self.assertIsNone(result)
    
    def test_zero(self):
        """нулевая высота. Должно работать корректно."""
        result = gen_bin_tree(0, 1)
        expected = {
            'value': 1,
            'left': None,
            'right': None
        }
        self.assertEqual(result, expected)

    def test_floating_point_height(self):
            """проверка на валидацию float. Тест провальный."""
            with self.assertRaises(TypeError):
                gen_bin_tree(2.5)  # Дробная высота

    def test_one(self):
        """высота 1. работает исправно."""
        result = gen_bin_tree(1, 1)
        expected = {
            'value': 1,
            'left': {
                'value': 2,
                'left': None,
                'right': None
            },
            'right': {
                'value': 4,
                'left': None,
                'right': None
            }
        }
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
