# тесты декоратора, тесты работы с StringIO.
import io 
from logger import logger
import unittest
from textwrap import dedent
import sys

class Test(unittest.TestCase):
    def test_setUp(self):
        expected = dedent('''Функция test_function начала работу с параметрами <BoundArguments (x=-1)>.
Функция test_function завершила свою работу с результатом: -22 

''')
        print(expected)
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def test_function(x):
            return x * 22
        test_function(-1)

        self.assertEqual(self.stream.getvalue(), expected)

    def test_error(self):
        expexted = dedent('''Функция divide_by_zero начала работу с параметрами <BoundArguments ()>.
!!!ФУНКЦИЯ divide_by_zero ЗАВЕРШИЛА СВОЮ РАБОТУ С ВОТ ЭТОЙ ОШИБКОЙ: ZeroDivisionError. ВОТ ТЕКСТ ЭТОЙ ОШИБКИ: division by zero 
''')
        self.stream = io.StringIO()
        @logger (handle = self.stream)
        def test_function(y):
            return 1 / y
        try:
            test_function(0)
        finally:
            self.assertEqual(self.stream.getvalue(), expexted)
        
if __name__ == "__main__":
    unittest.main()