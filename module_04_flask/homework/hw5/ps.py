"""
Напишите GET-эндпоинт /ps, который принимает на вход аргументы командной строки,
а возвращает результат работы команды ps с этими аргументами.
Входные значения эндпоинт должен принимать в виде списка через аргумент arg.

Например, для исполнения команды ps aux запрос будет следующим:

/ps?arg=a&arg=u&arg=x
"""
import shlex

from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route("/ps", methods=["GET"])
def ps() -> str:
    args: list[str] = request.args.getlist('arg')

    clean_user_cmd = shlex.quote(''.join(args))

    cleanest_cmd = shlex.split(clean_user_cmd)


    final_request = ['ps']
    final_request.extend(cleanest_cmd)

    result = subprocess.run(final_request, capture_output=True, text=True, encoding='cp866')
    ps_info = result.stdout.strip()

    return f'<pre>{ps_info}</pre>'

if __name__ == "__main__":
    app.run(debug=True)
