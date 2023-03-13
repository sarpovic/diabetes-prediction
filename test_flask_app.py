import unittest
from app import app
import random

class MyAppTestCase(unittest.TestCase):
    """
    This class contains the unit tests for the Flask application.
    """
    def setUp(self):
        """
        Sets up the Flask test client for use in the tests.
        """
        self.app = app.test_client()

    def test_home(self):
        """
        Tests the home page of the Flask application.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_predict(self):
        """
        Tests the prediction functionality of the Flask application.
        """
        data = {
            'pregnancies': random.randint(0,20),
            'glucose': random.randint(50,200),
            'bloodpressure': random.randint(50,200),
            'skinthickness': random.randint(10,50),
            'insulin': random.randint(20,900),
            'bmi': random.randint(20,50),
            'dpf': round(random.uniform(0.1, 3),1),
            'age': random.randint(15,100)
          
        }
        response = self.app.post('/predict', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Prediction:', response.data)

if __name__ == '__main__':
    """
    Runs the unit tests in the class.
    """
    suite = unittest.TestSuite()
    for i in range(50):
        suite.addTest(MyAppTestCase('test_home'))
        suite.addTest(MyAppTestCase('test_predict'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
