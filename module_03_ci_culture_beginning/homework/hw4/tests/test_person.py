
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
        try:  # TODO для таких случаев намного удобнее использовать self.assertRaises
            new_person = Person()
        except TypeError as context:
            # TODO в чем необходимость использовать такие "логи" для сообщений об ошибках тестов? Результат теста
            #  должен быть в рамках системы тестирования, то есть определяется встроенными инструментам self.assertTrue,
            #  self.assertFalse, self.assertRaises и т.д. Тогда результат тестировния может быть использован системой
            #  автоматизации деплоя, например (так называемая CI)
            self.error_file.write(f'## Ошибка: TypeError: {context}\n')
            self.error_file.write(
                '- **Причина**: при инициализации экземпляра класса не установлены значения для name и year_of_birth по умолчанию\n')
            self.error_file.write('- **Исправление**: установить значения по умолчанию name="" и year_of_birth=0\n')
            self.error_file.write('\n')


    def test_get_age_correct(self):
        fixed_now = datetime.datetime(2024, 12, 30)

        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = fixed_now
            try:
                self.assertEqual(self.person.get_age(), 34)
            except NameError as context:
                self.error_file.write(
                    f'## Ошибка: NameError: {context}\n')
                self.error_file.write(
                    '- **Причина**: Модуль datetime не импортирован\n')
                self.error_file.write('- **Исправление**: в разделе импортов модулей прописать import datetime\n')
                self.error_file.write('\n')

            except AssertionError as context:
                self.error_file.write(
                    f'## Ошибка: AssertionError: {context}\n')
                self.error_file.write(
                    '- **Причина**: в методе get_age неверно вычисляется возрастЖ нужно из текущего года вычитать год рождения\n')
                self.error_file.write('- **Исправление**: исправить вычисление возраста\n')
                self.error_file.write('\n')



    def test_get_name_correct(self):
        try:
            self.assertEqual(self.person.get_name(), 'Bob')
        except Exception as context:
            self.error_file.write(
                f'## Ошибка: AttributeError: {context}\n')
            self.error_file.write(
                '- **Причина**: В классе Person не определен атрибут name\n')
            self.error_file.write('- **Исправление**: В инициализации класса определить атрибут name, либо проверить корректность написания атрибута в методе get_name\n')
            self.error_file.write('\n')

    def test_set_name_correct(self):

        try:
            self.person.set_name('Piter')
            assert self.person.name == 'Piter'
        except AssertionError as context:
            self.error_file.write(
                f'## Ошибка: AssertionError: {context}\n')
            self.error_file.write(
                '- **Причина**: В методе set_name вместо присвоения значения аргумента name атрибуту self.name, происходит присвоение самого себя\n')
            self.error_file.write('- **Исправление**: Прописать в методе self.name = name\n')
            self.error_file.write('\n')

    def test_set_address_correct(self):

        try:
            self.person.set_address('Петрозаводск, Московская, 22 - 3')
            self.assertEqual(self.person.address, 'Петрозаводск, Московская, 22 - 3')
        except Exception:
            self.error_file.write(
                f'## Ошибка: Exception\n')
            self.error_file.write(
                '- **Причина**: В методе set_address вместо присвоения значения аргумента address атрибуту self.address происходит сравнение адрибута с аргументом\n')
            self.error_file.write('- **Исправление**: В методе set_address заменить "==" на "="\n')
            self.error_file.write('\n')

    def test_get_address_correct(self):

        try:
            self.assertEqual(self.person.get_address(), '')
        except Exception as context:
            self.error_file.write(
                f'## Ошибка: AttributeError: {context}\n')
            self.error_file.write(
                '- **Причина**: В классе Person не определен атрибут address\n')
            self.error_file.write('- **Исправление**: В инициализации класса определить атрибут address, либо проверить корректность написания атрибута в методе get_address\n')
            self.error_file.write('\n')

    def test_is_homeless_correct(self):
        try:
            self.assertEqual(self.person.is_homeless(), True)
        except NameError as context:
            self.error_file.write(
                f'## Ошибка: NameError: {context}\n')
            self.error_file.write(
                '-**Причина**: В методе is_homeless используется переменная address, но она не определена в контексте метода\n')
            self.error_file.write(
                '-**Исправление**: Вместо переменной address использовать атрибут self.address\n')
            self.error_file.write('\n')

        except Exception:
            self.error_file.write(
                f'## Ошибка: Exception')
            self.error_file.write(
                '-**Причина**: При инициализации объекта класса значение атрибута address по умолчанию пустая строка, а в методе is_homeless пустая строка сравнивается с None\n')
            self.error_file.write(
                '-**Исправление**: В методе is_homeless исправить код на return self.address == ""\n')
            self.error_file.write('\n')




    @classmethod
    def tearDownClass(cls):
        cls.error_file.close()