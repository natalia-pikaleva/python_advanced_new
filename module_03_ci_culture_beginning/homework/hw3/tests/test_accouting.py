from module_02_linux.homework.hw7.accounting import app, storage
import unittest
from pathlib import Path


class TestAccouting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        cls.storage = {'2024': {'10': 3789, '11': 2547, '12': 1358, 'total': 7694}}

    def test_correct_add(self):
        date = '20241231'
        expenses = str(1253)
        url = f'/add/{date}/{expenses}'
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual('Данные успешно добавлены', response.text)

    def test_correct_calculate_year(self):
        for year, info in self.storage.items():
            for month, expenses in info.items():
                date = year + month + '01'
                url = f'/add/{date}/{expenses}'
                response = self.app.get(url)

        year = '2024'

        url = f'/calculate/{year}'
        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(storage[year]['total']), response.text)

    def test_correct_calculate_month(self):
        for year, info in self.storage.items():
            for month, expenses in info.items():
                date = year + month + '01'
                url = f'/add/{date}/{expenses}'
                response = self.app.get(url)

        year = '2024'
        month = '11'
        url = f'/calculate/{year}/{month}'

        response = self.app.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.storage[year][month]), response.text)

    def test_incorrect_date_in_endpoint_add(self):
        date_list = ['241231', '2024-12-31', '31.12.24', 'date']
        expenses = str(1253)

        for date in date_list:
            url = f'/add/{date}/{expenses}'
            response = self.app.get(url)

            self.assertEqual(response.status_code, 200)

            self.assertIn('Неверный формат даты', response.data.decode())

    def test_date_with_flush_in_endpoint_add(self):
        date = '2024/12/31'
        expenses = str(1253)

        url = f'/add/{date}/{expenses}'
        response = self.app.get(url)

        self.assertEqual(response.status_code, 404)

    def test_calculates_with_storage_null(self):
        year = '1500'
        month = '01'

        url_list = [f'/calculate/{year}', f'/calculate/{year}{month}']

        for url in url_list:
            with self.subTest(url=url):
                response = self.app.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertIn('0', response.text)
