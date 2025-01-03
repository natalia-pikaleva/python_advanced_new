"""
Для каждого поля и валидатора в эндпоинте /registration напишите юнит-тест,
который проверит корректность работы валидатора. Таким образом, нужно проверить, что существуют наборы данных,
которые проходят валидацию, и такие, которые валидацию не проходят.
"""

import unittest
from hw1_registration import app


class TestRegistration(unittest.TestCase):
    def setUp(self):
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

    def test_correct_data(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567890,
            'index': 123456,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user test@example.com with phone +71234567890'.encode('utf-8'),
                      response.data)

    def test_miss_at_in_email(self):
        response = self.app.post('/registration', data={
            'email': 'testexample.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567890,
            'index': 123456,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'email': ['Invalid email address".encode('utf-8'),
                      response.data)

    def test_miss_point_in_email(self):
        response = self.app.post('/registration', data={
            'email': 'test@examplecom',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567890,
            'index': 123456,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'email': ['Invalid email address".encode('utf-8'),
                      response.data)

    def test_len_phone_more(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567890123,
            'index': 123456,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'phone':".encode('utf-8'),
                      response.data)

    def test_len_phone_less(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567,
            'index': 123456,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'phone':".encode('utf-8'),
                      response.data)

    def test_letters_in_phone(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': '12345678dd',
            'index': 123456,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'phone':".encode('utf-8'),
                      response.data)

    def test_miss_name(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'phone': 1234567890,
            'index': 123456,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'name': ['This field is required".encode('utf-8'),
                      response.data)

    def test_miss_index(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567890,
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'index': ['This field is required".encode('utf-8'),
                      response.data)

    def test_letters_in_index(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567890,
            'index': '1234ff',
            'comment': 'No name provided'
        })

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid input, {'index':".encode('utf-8'),
                      response.data)

    def test_miss_comment(self):
        response = self.app.post('/registration', data={
            'email': 'test@example.com',
            'address': 'Moscow street, 15',
            'name': 'Иванов И.И.',
            'phone': 1234567890,
            'index': 123456,
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully registered user test@example.com with phone +71234567890'.encode('utf-8'),
                      response.data)


if __name__ == '__main__':
    unittest.main()
