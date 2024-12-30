import unittest

from module_03_ci_culture_beginning.materials.testing_age.social_age import get_social_status



class TestSocialAge(unittest.TestCase):
    def test_if_can_get_child_status(self):
        age = 3
        expected_res = 'ребенок'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)


    def test_if_can_get_adult_status(self):
        age = 33
        expected_res = 'взрослый'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)


    def test_if_can_get_teenager_status(self):
        age = 16
        expected_res = 'подросток'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)


    def test_if_can_get_elderly_status(self):
        age = 55
        expected_res = 'пожилой'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)


    def test_if_can_get_retiree_status(self):
        age = 67
        expected_res = 'пенсионер'
        function_res = get_social_status(age)
        self.assertEqual(expected_res, function_res)

    def test_cannot_pass_negative_number(self):
        age = -15
        with self.assertRaises(ValueError):
            get_social_status(age)


    def test_cannot_pass_string_age(self):
        age = 'fgf'
        with self.assertRaises(ValueError):
            get_social_status(age)


if __name__ == '__main__':
    unittest.main()