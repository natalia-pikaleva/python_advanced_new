from module_03_ci_culture_beginning.homework.hw2.decrypt import decrypt
import unittest


class TextDecrypt(unittest.TestCase):

    def test_first_group_value(self):
        data_list = [
            'абра-кадабра.', 'абраа..-кадабра', 'абраа..-.кадабра', 'абра--..кадабра', 'абрау...-кадабра'
        ]
        for data in data_list:
            with self.subTest(data=data):
                decryption = decrypt(data)
                self.assertEqual(decryption, 'абра-кадабра')

    def test_second_group_value(self):
        data_list = [
            'абра........', '.', '1.......................'
        ]
        for data in data_list:
            with self.subTest(data=data):
                decryption = decrypt(data)
                self.assertEqual(decryption, '')

    def test_third_value(self):
        data = 'абр......a.'
        decryption = decrypt(data)
        self.assertEqual(decryption, 'a')

    def test_fourth_value(self):
        data = '1..2.3'
        decryption = decrypt(data)
        self.assertEqual(decryption, '23')

