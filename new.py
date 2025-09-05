from test import two_sum
import unittest

class TestMySolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(two_sum([0, 6], 6), [0, 1])

if __name__ ==  '__main__':
    unittest.main()