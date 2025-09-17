from main import two_sum
import unittest

class TestMySolution(unittest.TestCase):
    def test_first(self):
        self.assertEqual(two_sum([2,7,11,15], 9), [0, 1]) # этот тест должен выполняться хорошо без ошибок

    def test_second(self):
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2]) #этот тест тоже должен работать без ошибок

    def test_third(self):
        self.assertEqual(two_sum([3,3], 6), [0, 1]) # и это тоже должно быть верным
    def test_error_first(self):
            self.assertEqual(two_sum([0, 6.3], 6.3), [0, 1]) #здесь должна произойти поломка, т.к. число с плавающей точкой, а не int, как оно должно быть в условии.
    
if __name__ ==  '__main__':
    unittest.main()
