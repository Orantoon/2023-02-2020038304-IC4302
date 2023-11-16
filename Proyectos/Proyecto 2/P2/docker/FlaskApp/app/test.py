import unittest
import requests
import os
import app
from app import *

class test_api(unittest.TestCase):
    def test_login(self):
        url = 'http://