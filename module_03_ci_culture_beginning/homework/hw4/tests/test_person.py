import unittest
from unittest.mock import patch
import datetime
from module_03_ci_culture_beginning.homework.hw4.person import Person


class TestPerson(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.error_file = open('ERRORS.MD', 'a', encoding='utf8')
        cls.person = Person('Bob', 1990)

    def test__name_and_day_of_birth_is_none(self):
        with self.assertRaises(Exception) as context:
            new_person = Person()
        self.error_file.write(f'# Метод __init__\n')
        self.error_file.write(f'## Ошибка: {context.exception}\n')
        self.error_file.write('\n')

    def test_get_age_correct(self):
        now: datetime.datetime = datetime.datetime.now()

        with self.assertRaises(Exception) as context:
            self.assertEqual(self.person.get_age(), now.year - self.person.yob)

        self.error_file.write(f'# Метод get_age\n')
        self.error_file.write(
            f'## Ошибка:: {context.exception}\n')
        self.error_file.write('\n')

    def test_get_age_correct_value(self):
        now: datetime.datetime = datetime.datetime.now()

        with self.assertRaises(Exception) as context:
            self.assertEqual(self.person.get_age(), now.year - self.person.yob)

        self.error_file.write(f'# Метод get_age\n')
        self.error_file.write(
            f'## Ошибка:: {context.exception}\n')
        self.error_file.write('\n')

    def test_get_name_correct(self):
        self.assertEqual(self.person.get_name(), 'Bob')

    def test_set_name_correct(self):
        with self.assertRaises(Exception) as context:
            self.person.set_name('Piter')
            self.assertEqual(self.person.name, 'Piter')

        self.error_file.write(f'# Метод set_name\n')
        self.error_file.write(
            f'## Ошибка:: {context.exception}\n')
        self.error_file.write('\n')

    def test_set_address_correct(self):
        with self.assertRaises(Exception) as context:
            self.person.set_address('Петрозаводск, Мурманская, 22 - 3')
            self.assertEqual(self.person.address, 'Петрозаводск, Мурманская, 22 - 3')

        self.error_file.write(f'# Метод set_address\n')
        self.error_file.write(
            f'## Ошибка:: {context.exception}\n')
        self.error_file.write('\n')

    def test_get_address_correct(self):
        self.person.address = 'Петрозаводск, Московская, 22 - 3'
        self.assertEqual(self.person.get_address(), 'Петрозаводск, Московская, 22 - 3')

    def test_is_homeless_without_address_correct(self):
        piter = Person('Piter', 1992)
        with self.assertRaises(Exception) as context:
            self.assertEqual(self.person.is_homeless(), True)

        self.error_file.write(f'# Метод is_homeless\n')
        self.error_file.write(
            f'## Ошибка:: {context.exception}\n')
        self.error_file.write('\n')

    def test_is_homeless_with_address_correct(self):
        piter = Person('Piter', 1992, 'Петрозаодск, Октябрьская, 5 - 18')
        with self.assertRaises(Exception) as context:
            self.assertEqual(self.person.is_homeless(), False)

        self.error_file.write(f'# Метод is_homeless\n')
        self.error_file.write(
            f'## Ошибка:: {context.exception}\n')
        self.error_file.write('\n')

    @classmethod
    def tearDownClass(cls):
        cls.error_file.close()
