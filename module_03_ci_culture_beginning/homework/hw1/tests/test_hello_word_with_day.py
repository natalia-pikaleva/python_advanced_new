import unittest
from freezegun import freeze_time
import datetime

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

    @freeze_time("2024-12-30")
    def test_weekday_is_monday(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Привет, Наталья. Хорошего понедельника!', response.text)

    @freeze_time("2024-12-31")
    def test_weekday_is_tuesday(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Привет, Наталья. Хорошего вторника!', response.text)

    @freeze_time("2025-01-01")
    def test_weekday_is_wednesday(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Привет, Наталья. Хорошей среды!', response.text)

    @freeze_time("2025-01-02")
    def test_weekday_is_thursday(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Привет, Наталья. Хорошего четверга!', response.text)

    @freeze_time("2025-01-03")
    def test_weekday_is_friday(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Привет, Наталья. Хорошей пятницы!', response.text)

    @freeze_time("2025-01-04")
    def test_weekday_is_saturday(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Привет, Наталья. Хорошей субботы!', response.text)

    @freeze_time("2025-01-05")
    def test_weekday_is_sunday(self):
        response = self.app.get('/hello-world/Наталья')
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Привет, Наталья. Хорошего воскресенья!', response.text)
# TODO Чтобы не дублировать код теста, используйте цикл и контекстный менеджер (общий c self.subTest, тогда
#  при первом неверном assert тест не завершится, а выполнятся все "кейсы" и будет отчёт для каких значений
#  тесты провалились, а для каких были успешны)
