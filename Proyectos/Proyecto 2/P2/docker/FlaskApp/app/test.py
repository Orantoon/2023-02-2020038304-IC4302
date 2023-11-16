import unittest
import requests
import os
import app
from app import *
import json

URL = 'https://18tkx655-5001.euw.devtunnels.ms/'

class test_api(unittest.TestCase):
    def test_login(self):
        headers = {
            'Content-Type': 'application/json', 
        }

        credentials = json.dumps({
            "email": "unittest@estudiantec.cr",
            "password": "unittest"
        })

        # Proporcionar los encabezados como un parámetro adicional en la solicitud post
        response = requests.post(URL+"login", data=credentials, headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_getMovies(self):
        response = requests.get(URL+"neo4j/search/Matrix")
        self.assertEqual(response.status_code, 200)

    def test_castAsActor(self):
        response = requests.get(URL+"neo4j/castAsActor/Tom Hanks")
        self.assertEqual(response.status_code, 200)

    def test_castAsDirector(self):
        response = requests.get(URL+"neo4j/castAsDirector/Tom Hanks")
        self.assertEqual(response.status_code, 200)

    def test_directorAsDirector(self):
        response = requests.get(URL+"neo4j/directorAsDirector/Tom Hanks")
        self.assertEqual(response.status_code, 200)

    def test_directorAsActor(self):
        response = requests.get(URL+"neo4j/directorAsActor/Tom Hanks")
        self.assertEqual(response.status_code, 200)




if __name__=="__main__":
   unittest.main()