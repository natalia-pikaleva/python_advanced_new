"""
Напишите GET-эндпоинт /uptime, который в ответ на запрос будет выводить строку вида f"Current uptime is {UPTIME}",
где UPTIME — uptime системы (показатель того, как долго текущая система не перезагружалась).

Сделать это можно с помощью команды uptime.
"""

from flask import Flask
import subprocess
import re

app = Flask(__name__)


@app.route("/uptime", methods=['GET'])
def _uptime() -> str:
    result = subprocess.run(['systeminfo'], capture_output=True, text=True, encoding='cp866')
    uptime_info = result.stdout.strip()

    match = re.search(r'Время загрузки системы:\s+(.*)', uptime_info)

    if match:
        uptime = match.group(1)
        return f"Current uptime is {uptime}"
    else:
        return "Could not retrieve uptime information."


if __name__ == '__main__':
    app.run(debug=True)
