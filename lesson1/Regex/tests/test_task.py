import unittest
from ..task import answer


class TestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(answer, "1.1", msg="True")
