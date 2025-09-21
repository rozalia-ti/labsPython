from main import mainFunc
import unittest

class TestMySolution(unittest.TestCase):
    def test_normal_1(self):
        """обыкновенный тест с положительными значениями"""
        self.assertEqual(mainFunc(7, 3, 243), [7, 8])
    def test_normal_2(self):
        """тест с отрицательными значениями"""
        self.assertEqual(mainFunc(449, -123, 3433), [449, 10])
    def test_error_1(self):
        """тест с заведомой ошибкой, в терминале выводит вот такое: line 29, in guess if arr[mid] < target:"""
        self.assertEqual(mainFunc(5, 43, 100), [43, 6])
    def test_error_2(self):
        """тест с заведомой ошибкой ввода типизации. В терминале выводит TypeError: 'float' object cannot be interpreted as an integer"""
        self.assertEqual(mainFunc(5.4, 32.23, 100), [32.23, 4])

if __name__ == '__main__':
    unittest.main()
