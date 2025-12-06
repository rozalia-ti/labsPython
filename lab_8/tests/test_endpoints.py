import unittest
import requests

ROOT = "http://localhost:8088/"

class Test(unittest.TestCase):
    def test_root(self):
        resp = requests.get(ROOT)
        self.assertEqual(resp.status_code, 200)

    def test_users(self):
        resp = requests.get(ROOT + "users")
        self.assertEqual(resp.status_code, 200)

    def test_currencies(self):
        resp = requests.get(ROOT + "currencies")
        self.assertEqual(resp.status_code, 200)

    def test_author(self):
        resp = requests.get(ROOT + "author")
        self.assertEqual(resp.status_code, 200)

if __name__ == "__main__":
    unittest.main()
