import unittest
from task import ans

print(ans)

class TestCase(unittest.TestCase):
    def test_add(self):
        answer = "Mervyn Peake"
        self.assertEqual(ans, answer, msg="True")
