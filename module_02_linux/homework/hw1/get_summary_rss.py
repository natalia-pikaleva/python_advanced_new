"""
С помощью команды ps можно посмотреть список запущенных процессов.
С флагами aux эта команда выведет информацию обо всех процессах, запущенных в системе.

Запустите эту команду и сохраните выданный результат в файл:

$ ps aux > output_file.txt

Столбец RSS показывает информацию о потребляемой памяти в байтах.

Напишите функцию get_summary_rss, которая на вход принимает путь до файла с результатом выполнения команды ps aux,
а возвращает суммарный объём потребляемой памяти в человекочитаемом формате.
Это означает, что ответ надо перевести в байты, килобайты, мегабайты и так далее.
"""


def get_summary_rss(ps_output_file_path: str) -> str:
    '''
    Функция принимает на входе путь до файла output_file.txt и возвращает объем потребляемой памяти
    в человекочитаемом формате
    :param ps_output_file_path: путь до файла
    :return: объем потребляемой памяти
    в человекочитаемом формате
    '''
    summary_rss = 0
    with open(ps_output_file_path, 'r') as file:
        next(file)
        for i_line in file:
            list_info = i_line.split()
            summary_rss += int(list_info[5])

    for unit in ['B', 'KB', 'MB', 'GB']:
        if summary_rss < 1024:
            return f"{summary_rss:.2f} {unit}"
        summary_rss /= 1024
    return f"{summary_rss:.2f} TB"


if __name__ == '__main__':
    path: str = 'output_file.txt'
    summary_rss: str = get_summary_rss(path)
    print(summary_rss)
