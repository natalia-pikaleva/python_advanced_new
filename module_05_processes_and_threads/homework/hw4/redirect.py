"""
Иногда возникает необходимость перенаправить вывод в нужное нам место внутри программы по ходу её выполнения.
Реализуйте контекстный менеджер, который принимает два IO-объекта (например, открытые файлы)
и перенаправляет туда стандартные потоки stdout и stderr.

Аргументы контекстного менеджера должны быть непозиционными,
чтобы можно было ещё перенаправить только stdout или только stderr.
"""

from types import TracebackType
from typing import Type, Literal, IO
import sys
import traceback


class Redirect:
    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.new_stdout = stdout if stdout is not None else sys.stdout
        self.new_stderr = stderr if stderr is not None else sys.stderr

    def __enter__(self):
        sys.stdout = self.new_stdout
        sys.stderr = self.new_stderr

        return sys.stdout, sys.stderr

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> bool:

        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

        if self.new_stdout is not None and self.new_stdout is not sys.stdout:
            self.new_stdout.close()
        if self.new_stderr is not None and self.new_stderr is not sys.stderr:
            self.new_stderr.close()

        return False



print('Hello stdout')
stdout_file = open('stdout.txt', 'w')
stderr_file = open('stderr.txt', 'w')


with Redirect(stdout=stdout_file, stderr=stderr_file):
    try:
        print('Hello stdout.txt')
        raise Exception('Hello stderr.txt')
    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)



print('Hello stdout again')
# raise Exception('Hello stderr')

stdout_file.close()
stderr_file.close()