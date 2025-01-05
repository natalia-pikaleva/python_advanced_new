import subprocess

import subprocess
import shlex
import json
import time


def run_program():
    start = time.time()
    proc = subprocess.Popen(
            'sleep 10 && exit 1',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

    try:
        # Ждем 9 секунд
        proc.wait(timeout=9)
        print("Процесс завершился до истечения времени ожидания.")
    except subprocess.TimeoutExpired:
        print("Процесс все еще работает после 9 секунд.")
        output, errors = proc.communicate()  # Получаем вывод и ошибки
        if proc.returncode == 0:
            print('Process with PID {} ended successfully'.format(proc.pid))
            print(output.decode().strip())  # Выводим результат
        else:
            print('Process with PID {} failed with error: {}'.format(proc.pid, errors.decode().strip()))

    print('Done in {}'.format(time.time() - start))


if __name__ == '__main__':
    run_program()
