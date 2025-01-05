import unittest
from redirect import Redirect
import traceback
import sys
from unittest.mock import mock_open, patch


class TestRedirect(unittest.TestCase):
    # Тест проверяет корректность работы контекстного менеджера
    def test_correct_work(self):
        with open('test_stdout.txt', 'w') as stdout_file, open('test_stderr.txt', 'w') as stderr_file:
            with Redirect(stdout=stdout_file, stderr=stderr_file):
                print('Test stdout.txt')
                try:
                    raise Exception('Test stderr.txt')
                except Exception:
                    traceback.print_exc(file=sys.stderr)

        with open('test_stdout.txt', 'r') as stdout_file:
            stdout_content = stdout_file.read()
            self.assertEqual(stdout_content.strip(), 'Test stdout.txt')

        with open('test_stderr.txt', 'r') as stderr_file:
            stderr_content = stderr_file.read()
            self.assertIn('Test stderr.txt', stderr_content)

    # Тест проверяет корректность работы, если stdout=None
    def test_correct_work_without_stdout_file(self):
        with open('test_stderr.txt', 'w') as stderr_file:
            with Redirect(stderr=stderr_file):
                try:
                    raise Exception('Test stderr.txt')
                except Exception:
                    traceback.print_exc(file=sys.stderr)

        with open('test_stderr.txt', 'r') as stderr_file:
            stderr_content = stderr_file.read()
            self.assertIn('Test stderr.txt', stderr_content)

    # Тест проверяет корректность работы, если stderr=None
    def test_correct_work_without_stderr_file(self):
        with open('test_stdout.txt', 'w') as stdout_file:
            with Redirect(stdout=stdout_file):
                print('Test stdout.txt')

        with open('test_stdout.txt', 'r') as stdout_file:
            stdout_content = stdout_file.read()
            self.assertEqual(stdout_content.strip(), 'Test stdout.txt')

    # Тест проверяет корректность работы, если stdout=None и stderr=None
    def test_redirect_with_none_streams(self):
        with Redirect(stdout=None, stderr=None):
            try:
                with Redirect(stdout=None, stderr=None):
                    print('This should not be printed anywhere.')
                    raise Exception('This should not be printed anywhere either.')
            except Exception as e:
                self.assertEqual(str(e), 'This should not be printed anywhere either.')

    # Тест проверяет закрыты ли файлы после окончания работы контекстного менеджера
    def test_file_closing(self):
        mock_stdout = mock_open()
        mock_stderr = mock_open()

        with patch('builtins.open', mock_stdout), patch('builtins.open', mock_stderr):
            with Redirect(stdout=mock_stdout(), stderr=mock_stderr()):
                print('Test output')

        mock_stdout().close.assert_called_once()
        mock_stderr().close.assert_called_once()

    # Тест проверяет перенаправления в файлы с существующим содержимым
    def test_overwriting_existing_file(self):
        with open('test_stdout.txt', 'w') as f:
            f.write('Old content\n')

        with open('test_stderr.txt', 'w') as f:
            f.write('Old error\n')

        with open('test_stdout.txt', 'a') as stdout_file, open('test_stderr.txt', 'a') as stderr_file:
            with Redirect(stdout=stdout_file, stderr=stderr_file):
                print('New content')
                try:
                    raise Exception('New error')
                except Exception:
                    traceback.print_exc(file=sys.stderr)

        with open('test_stdout.txt', 'r') as stdout_file:
            self.assertEqual(stdout_file.read().strip(), 'Old content\nNew content')

        with open('test_stderr.txt', 'r') as stderr_file:
            self.assertIn('New error', stderr_file.read())

    # Тест проверяет корректную обработку исключений
    def test_exception_handling(self):
        try:
            with Redirect():
                raise Exception("Test exception")
        except Exception as e:
            self.assertEqual(str(e), "Test exception")


if __name__ == '__main__':
    with open('test_results.txt', 'a') as test_file_stream:
        runner = unittest.TextTestRunner(stream=test_file_stream)
        unittest.main(testRunner=runner)
