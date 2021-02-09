import unittest
from python_repos import r


class TestStatusCode(unittest.TestCase):

    def test_status_ok(self):
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
