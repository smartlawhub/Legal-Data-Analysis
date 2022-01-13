import unittest
from task import answer

# todo: replace this with an actual test
class TestCase(unittest.TestCase):
    def test_add(self):
        self.assertEqual(answer, 41, msg="Should be the number of files you changed")
