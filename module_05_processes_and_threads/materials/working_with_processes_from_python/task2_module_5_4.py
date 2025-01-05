import subprocess

import subprocess
import shlex
import json


def get_ip_address():
    # Команда для выполнения
    command = 'curl -i -H "Accept: application/json" -X GET https://api.ipify.org?format=json'

    # Токенизация команды
    args = shlex.split(command)

    print(f'args: {args}')

    # Запуск команды и получение вывода
    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print(f'result: {result}')

    # Проверка на наличие ошибок
    if result.returncode != 0:
        raise Exception(f"Error executing command: {result.stderr.decode()}")

    # Парсинг JSON-вывода
    output = result.stdout.decode()
    print(f'output: {output}')

    json_output = json.loads(output.split('\r\n\r\n')[1])  # Извлечение тела ответа
    print(f'json_output: {json_output}')

    return json_output['ip']  # Возвращаем IP-адрес




if __name__ == '__main__':
    ip_address = get_ip_address()
    print(f"My IP address is: {ip_address}")