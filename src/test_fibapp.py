import unittest
import fib
import fib_app
import json

class TestFibonacci(unittest.TestCase):
    def test_fib_zero(self):
        self.assertEqual(fib.fib_number(0), 0, "Should be 0")
    
    def test_fib_one(self):
        self.assertEqual(fib.fib_number(1), 1, "Should be 1")

    def test_fib_positive(self):
        self.assertEqual(fib.fib_number(6), 8, "Should be 8")

    def test_fib_negative(self):
        self.assertRaises(ValueError, fib.fib_number, -21)

    def test_sequence_empty(self):
        self.assertEqual(len(fib.fib_sequence(0)), 0)

    def test_sequence_positive(self):
        self.assertEqual(fib.fib_sequence(5), [0, 1, 1, 2, 3])

    def test_fib_negative(self):
        self.assertRaises(ValueError, fib.fib_sequence, -5)

class FlaskTest(unittest.TestCase):
    def setUp(self):
        fib_app.app.testing = True
        self.client = fib_app.app.test_client()
        fib_app.app.logger.disabled = True

    def test_seq_positive_number(self):
        response = self.client.get('/fibseq/5')

        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

        content = json.loads(response.data)
        self.assertEqual(content['error'], None)
        self.assertEqual(content['sequence'], [0, 1, 1, 2, 3])

    def test_seq_negative_number(self):
        response = self.client.get('/fibseq/-20')

        self.assertEqual(response.status_code, 400)
        self.assertIn('application/json', response.content_type)

        content = json.loads(response.data)
        self.assertIn('Negative value', content['error'])
        self.assertEqual(content['sequence'], None)

    def test_seq_string_input(self):
        response = self.client.get('/fibseq/abc')

        self.assertEqual(response.status_code, 400)
        self.assertIn('application/json', response.content_type)

        content = json.loads(response.data)
        self.assertIn('invalid literal', content['error'])
        self.assertEqual(content['sequence'], None)


if __name__ == "__main__":
    unittest.main()
