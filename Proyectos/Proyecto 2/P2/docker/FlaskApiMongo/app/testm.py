import unittest
import json
from app import app

class TestGeneral(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
          self.app = app.test_client(self)
          super().__init__(methodName)
        
    def test1(self):
            response = self.app.get('/mongo/search/Keanu Reeves')
            self.assertEqual(200, response.status_code, msg=f"{response.status_code}")
            self.assertNotEqual(0, len(response.json[0]), msg=f"Test fail: Len of the document equal to cero {response.json[0]}")
            print("Test 1 Completed")

            
    def test2(self):
            response = self.app.get('/mongo/searchCast/Keanu Reeves')
            self.assertEqual(200, response.status_code, msg=f"{response.status_code}")
            self.assertNotEqual(0, len(response.json[0]), msg=f"Test fail {len(response.json)}")
            print("Test 2 complete")
    
    def testAd(self):
        response = self.app.get('/mongo/searchDirector/Andy Wachowski')
        self.assertEqual(200, response.status_code, msg=f"{response.status_code}")
        self.assertNotEqual(0, len(response.json[0]), msg=f"Test fail, datos: {response.json[0]}")
        print("Test 3 complete") 
    def test4(self):
        response = self.app.get('/mongo/pelicula/The Matrix')
        self.assertEqual(200, response.status_code, msg=f"{response.status_code}")
        self.assertNotEqual(0, len(response.json[0]), msg=f"Test fail, datos: {response.json[0]}")
        print("Test 4 complete")                          
        
if __name__== "__main__":
    unittest.main()