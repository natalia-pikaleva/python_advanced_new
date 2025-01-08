"""
Каждый лог содержит в себе метку времени, а значит, правильно организовав логирование,
можно отследить, сколько времени выполняется функция.

Программа, которую вы видите, по умолчанию пишет логи в stdout. Внутри неё есть функция measure_me,
в начале и в конце которой пишется "Enter measure_me" и "Leave measure_me".
Сконфигурируйте логгер, запустите программу, соберите логи и посчитайте среднее время выполнения функции measure_me.
"""
import logging
import random
import datetime
from typing import List
import json

logger = logging.getLogger(__name__)

from datetime import datetime, timedelta


class JsonAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        current_time = datetime.now().isoformat()

        log_entry = {
            "time": current_time,
            "message": msg
        }
        return json.dumps(log_entry, ensure_ascii=False), kwargs


def get_data_line(sz: int) -> List[int]:
    try:
        logger.debug("Enter get_data_line")
        return [random.randint(-(2 ** 31), 2 ** 31 - 1) for _ in range(sz)]
    finally:
        logger.debug("Leave get_data_line")


def measure_me(nums: List[int]) -> List[List[int]]:
    logger.info("Enter measure_me")
    results = []
    nums.sort()

    for i in range(len(nums) - 2):
        logger.debug(f"Iteration {i}")
        left = i + 1
        right = len(nums) - 1
        target = 0 - nums[i]
        if i == 0 or nums[i] != nums[i - 1]:
            while left < right:
                s = nums[left] + nums[right]
                if s == target:
                    logger.debug(f"Found {target}")
                    results.append([nums[i], nums[left], nums[right]])
                    logger.debug(
                        f"Appended {[nums[i], nums[left], nums[right]]} to result"
                    )
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif s < target:
                    logger.debug(f"Increment left (left, right) = {left, right}")
                    left += 1
                else:
                    logger.debug(f"Decrement right (left, right) = {left, right}")

                    right -= 1

    logger.info("Leave measure_me")

    return results

if __name__ == "__main__":
    logging.basicConfig(level="INFO", filename="stder.txt", format='%(message)s', encoding="utf-8")
    logger = JsonAdapter(logging.getLogger(__name__))
    for it in range(15):
        data_line = get_data_line(10 ** 3)
        measure_me(data_line)

    sum_time_total = timedelta(0)
    count_total = 0

    try:
        with open('stder.txt', "r", encoding='utf8') as fi:
            for i_line in fi.readlines():
                i_log = json.loads(i_line)
                if i_log['message'] == 'Enter measure_me':
                    start_time = datetime.strptime(i_log['time'], "%Y-%m-%dT%H:%M:%S.%f")
                elif i_log['message'] == 'Leave measure_me':
                    sum_time_total = sum_time_total + datetime.strptime(i_log['time'], "%Y-%m-%dT%H:%M:%S.%f") - start_time
                    count_total += 1
            if count_total > 0:
                average_time = sum_time_total / count_total
                print(f'Среднее время выполнения функции measure_me: {average_time}')
            else:
                print('Функция measure_me не выполнилась ни разу')

    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")