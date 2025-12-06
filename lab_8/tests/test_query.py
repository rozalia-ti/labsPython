import unittest
from urllib.parse import urlparse, parse_qs


class Test(unittest.TestCase):
    def test_qs1(self):
        path = "/user?id=123"
        parsed_url = urlparse(path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        user_id = int(query_params['id'][0])

        self.assertEqual(user_id, 123)

    def test_qs2(self):
        path = "/user/?id=123"
        parsed_url = urlparse(path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        user_id = int(query_params['id'][0])

        self.assertEqual(user_id, 123)

if __name__ == "__main__":
    unittest.main()
