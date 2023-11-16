import unittest
import requests
import os
import app
from app import *
import json

class test_api(unittest.TestCase):
    def test_login(self):
        url = 'https://18tkx655-5001.euw.devtunnels.ms/login'
        credentials =json.dumps({
                        "email": "joctan@estudiantec.cr",
                        "password":" 12345"
                    })
        response = requests.post(url,credentials)
        self.assertEqual(response.status_code, 200)




if __name__=="__main__":
   unittest.main()
                        