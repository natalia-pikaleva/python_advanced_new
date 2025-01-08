"""
Ваш коллега, применив JsonAdapter из предыдущей задачи, сохранил логи работы его сайта за сутки
в файле skillbox_json_messages.log. Помогите ему собрать следующие данные:

1. Сколько было сообщений каждого уровня за сутки.
2. В какой час было больше всего логов.
3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
4. Сколько сообщений содержит слово dog.
5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
"""
import subprocess
from typing import Dict
import json
from collections import Counter
from datetime import datetime


def task1() -> Dict[str, int]:
    """
    1. Сколько было сообщений каждого уровня за сутки.
    @return: словарь вида {уровень: количество}
    """
    message_dict = {}

    for i_log in log_data:
        if i_log['level'] in message_dict:
            message_dict[i_log['level']] += 1
        else:
            message_dict[i_log['level']] = 1

    return message_dict


def task2() -> int:
    """
    2. В какой час было больше всего логов.
    @return: час
    """

    hour_counter = Counter()

    for log in log_data:
        time_str = log["time"]
        time_obj = datetime.strptime(time_str, "%H:%M:%S")

        hour_counter[time_obj.hour] += 1

    most_common_hour, count = hour_counter.most_common(1)[0]

    return most_common_hour


def task3() -> int:
    """
    3. Сколько логов уровня CRITICAL было в период с 05:00:00 по 05:20:00.
    @return: количество логов
    """
    grep_time = ['grep', '-E', '"time": "05:(0[0-9]:[0-9]{2}|1[0-9]:[0-9]{2}|20:00:00)"', 'skillbox_json_messages.log']

    process_time = subprocess.Popen(grep_time, stdout=subprocess.PIPE)

    grep_level = ['grep', '-c', '"level": "CRITICAL"']

    process_level = subprocess.Popen(grep_level, stdin=process_time.stdout, stdout=subprocess.PIPE)

    process_time.stdout.close()

    output, error = process_level.communicate()

    if output:
        return output.decode('utf-8')
    else:
        return f"No matching logs found."


def task4() -> int:
    """
    4. Сколько сообщений содержат слово dog.
    @return: количество сообщений
    """
    grep_dog = ['grep', '-E', '-c', 'dog', 'skillbox_json_messages.log']

    process = subprocess.Popen(grep_dog, stdout=subprocess.PIPE)

    output, error = process.communicate()

    if output:
        return output.decode('utf-8')
    else:
        return f"No matching logs found."


def task5() -> str:
    """
    5. Какое слово чаще всего встречалось в сообщениях уровня WARNING.
    @return: слово
    """
    grep_level = ['grep', '"level": "WARNING"', 'skillbox_json_messages.log']

    process_level = subprocess.Popen(grep_level, stdout=subprocess.PIPE)

    output, error = process_level.communicate()

    if output:

        data_warning = output.decode('utf-8').splitlines()

        words_counter = Counter()

        for log in data_warning:
            try:
                log_data = json.loads(log)
                message = log_data.get("message", "")

                if isinstance(message, str):
                    words_list = message.split()
                    for word in words_list:
                        words_counter[word] += 1


            except (json.JSONDecodeError, KeyError):
                continue

        if words_counter:
            most_common_word, count = words_counter.most_common(1)[0]
            return most_common_word

    else:
        return f"No matching logs found."


if __name__ == '__main__':
    log_data = []
    try:
        with open('skillbox_json_messages.log', "r", encoding='utf8') as fi:
            for i_line in fi.readlines():
                i_log = json.loads(i_line)
                log_data.append(i_log)

    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")

    tasks = (task1, task2, task3, task4, task5)
    for i, task_fun in enumerate(tasks, 1):
        task_answer = task_fun()
        print(f'{i}. {task_answer}')
