
import unittest
from Controller import *

class TestStringsMethods(unittest.TestCase):
    def test_controller(self):
        self.assertEqual(controller('https://api.biorxiv.org/covid19/0'), (919))

unittest.main()
