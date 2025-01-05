import unittest
from block_errors import BlockErrors


class TestBlockErrors(unittest.TestCase):
    def test_must_skip_error(self):
        with self.assertRaises(ZeroDivisionError):
            with BlockErrors({TypeError}):
                a = 1 / 0

    def test_ignored_error(self):
        try:
            with BlockErrors({ZeroDivisionError}):
                a = 1 / 0
        except:
            self.fail()

    def test_skip_error_up_and_ignored(self):
        try:
            outer_err_types = {TypeError}
            with BlockErrors(outer_err_types):
                inner_err_types = {ZeroDivisionError}
                with BlockErrors(inner_err_types):
                    a = 1 / '0'
        except:
            self.fail()

    def test_subsidiary_error_ignored(self):
        try:
            err_types = {Exception}
            with BlockErrors(err_types):
                a = 1 / '0'
        except:
            self.fail()


if __name__ == '__main__':
    unittest.main()
