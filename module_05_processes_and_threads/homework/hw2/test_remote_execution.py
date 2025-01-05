import unittest
from remote_execution import app


class TestRemoteExecution(unittest.TestCase):
    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()
        self.app.testing = True

    def test_correct_work(self):
        response = self.app.post('/run_code', data={'code': 'print("Hello, world!")', 'timeout': 5})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello, world", response.get_json()["output"])

    def test_timeout_more_than_time_of_app(self):
        response = self.app.post('/run_code', data={'code': 'import time; time.sleep(5)', 'timeout': 10})
        self.assertEqual(response.status_code, 200)

    def test_timeout_less_than_time_of_app(self):
        response = self.app.post('/run_code', data={'code': 'import time; time.sleep(15)', 'timeout': 10})
        self.assertEqual(response.status_code, 500)
        self.assertIn("Process timed out", response.text)

    def test_incorrect_command(self):
        response = self.app.post('/run_code', data={'code': '1/0', 'timeout': 10})
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.text)

    def test_invalid_code(self):
        response = self.app.post('/run_code', data={'timeout': 10})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'code': ['This field is required", response.text)

    def test_invalid_timeout(self):
        response = self.app.post('/run_code', data={'code': 'print("Hello, world!")'})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'timeout': ['This field is required", response.text)

    def test_incorrect_timeout(self):
        timeout_list = [-5, 55]
        for timeout in timeout_list:
            with self.subTest(timeout=timeout):
                response = self.app.post('/run_code', data={'code': 'print("Hello, world!")', 'timeout': timeout})
                self.assertEqual(response.status_code, 400)
                self.assertIn("Invalid input, {'timeout': ['Number must be between 0 and 30.'", response.text)

if __name__ == '__main__':
    unittest.main()
