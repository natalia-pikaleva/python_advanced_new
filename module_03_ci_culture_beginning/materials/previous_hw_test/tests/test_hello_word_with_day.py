import unittest

from flask import Flask

from module_03_ci_culture_beginning.materials.previous_hw_test.hello_word_with_day import app

from unittest.mock import patch
from datetime import datetime


class HelloWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        response = self.app.get('/hello-world/Иван')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Привет, Иван.' in response.text)

    @patch('module_03_ci_culture_beginning.materials.previous_hw_test.hello_word_with_day.datetime')
    def test_greetings_by_weekday(self, mock_datetime):
        greetings = (
            'Хорошего понедельника',
            'Хорошего вторника',
            'Хорошей среды',
            'Хорошего четверга',
            'Хорошей пятницы',
            'Хорошей субботы',
            'Хорошего воскресенья'
        )

        for weekday in range(7):
            mock_datetime.today.return_value = datetime(2021, 1, weekday + 4)  # Пн - Вс
            response = self.app.get('/hello-world/Иван')
            self.assertIn(greetings[weekday].encode(), response.data)

    def test_empty_name(self):
        response = self.app.get('/hello-world/')
        self.assertEqual(response.status_code, 404)
