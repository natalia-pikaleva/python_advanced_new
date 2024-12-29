"""
Удобно направлять результат выполнения команды напрямую в программу с помощью конвейера (pipe):

$ ls -l | python3 get_mean_size.py

Напишите функцию get_mean_size, которая на вход принимает результат выполнения команды ls -l,
а возвращает средний размер файла в каталоге.
"""

import sys


def get_mean_size(ls_output: str) -> float:
    '''
    Функция принимает на входе строки ls_output, в которых содержится
    информация обо всех файлах и папках директории, и возвращает средний
    размер файла в каталоге
    :param ls_output:
    :return:
    '''
    total_summ = 0
    total_count = 0

    for i_line in ls_output:
        list_info = i_line.split()

        try:
            if list_info[0].startswith('-rwx'):
                total_summ += int(list_info[4])
                total_count += 1
        except Exception:
            pass
    if total_count == 0:
        return 0.0

    average_size = round(total_summ / total_count, 2)

    return average_size


if __name__ == '__main__':
    data: str = sys.stdin.readlines()
    mean_size: float = get_mean_size(data)
    print(mean_size)
