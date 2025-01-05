import subprocess

import subprocess
import shlex
import json
import time


def run_program():
    start = time.time()
    procs = []
    for pnum in range(1, 11):
        p = subprocess.Popen(
            'sleep 15 && echo "My mission is done here!"',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        print('Process number {} started. PID: {}'.format(
            pnum, p.pid
        ))
        procs.append(p)

    for proc in procs:
        output, errors = proc.communicate()  # Получаем вывод и ошибки
        if proc.returncode == 0:
            print('Process with PID {} ended successfully'.format(proc.pid))
            print(output.decode().strip())  # Выводим результат
        else:
            print('Process with PID {} failed with error: {}'.format(proc.pid, errors.decode().strip()))

    print('Done in {}'.format(time.time() - start))


if __name__ == '__main__':
    run_program()
