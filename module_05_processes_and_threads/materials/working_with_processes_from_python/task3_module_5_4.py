import subprocess

import subprocess
import shlex
import json


def count_process():
    # Команда для выполнения
    command = 'ps -A'

    # Токенизация команды
    args = shlex.split(command)

    # Запуск команды и получение вывода
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Проверка на наличие ошибок
    if result.returncode != 0:
        raise Exception(f"Error executing command: {result.stderr.decode()}")

    # Получаем вывод и разбиваем его на строки
    output = result.stdout.decode()
    lines = output.strip().split('\n')

    # Количество процессов - это количество строк минус одна (заголовок)
    process_count = len(lines) - 1  # Убираем заголовок

    return process_count

if __name__ == '__main__':
    print(f'Количество запущенных процессов: {count_process()}')