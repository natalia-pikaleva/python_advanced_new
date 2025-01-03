import unittest
from freezegun import freeze_time

from module_03_ci_culture_beginning.homework.hw1.hello_word_with_day import app


class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_hello_world(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Привет, Наталья', response.text)

    def test_empty_name(self):
        response = self.app.get('/hello-world/')
        self.assertEqual(response.status_code, 404)

    def test_weekday_greetings(self):
        test_cases = [
            ("2024-12-30", "Привет, Наталья. Хорошего понедельника!"),
            ("2024-12-31", "Привет, Наталья. Хорошего вторника!"),
            ("2025-01-01", "Привет, Наталья. Хорошей среды!"),
            ("2025-01-02", "Привет, Наталья. Хорошего четверга!"),
            ("2025-01-03", "Привет, Наталья. Хорошей пятницы!"),
            ("2025-01-04", "Привет, Наталья. Хорошей субботы!"),
            ("2025-01-05", "Привет, Наталья. Хорошего воскресенья!")
        ]

        for frozen_time, expected_greeting in test_cases:
            with freeze_time(frozen_time):
                with self.subTest(frozen_time=frozen_time):
                    response = self.app.get('/hello-world/Наталья')
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.text, expected_greeting)

