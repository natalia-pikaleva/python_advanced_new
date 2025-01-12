import json
from flask import Flask, request

app = Flask(__name__)


@app.route('/log', methods=['POST'])
def log():
    """
    Записываем полученные логи которые пришли к нам на сервер
    return: текстовое сообщение об успешной записи, статус код успешной работы

    """
    print('Что-то отправлено')
    try:
        data = request.get_json(force=True)
    except Exception as ex:
        print(f'Ошибка {ex}')
        return f'Ошибка {ex}', 400

    if data is None:
        data = request.data.decode('utf-8')

    if data:
        with open('log_file.txt', "a") as file:
            file.write(str(data) + '\n')

        return 'OK', 200
    else:
        return 'Bad Request', 400


@app.route('/logs', methods=['GET'])
def logs():
    """
    Рендерим список полученных логов
    return: список логов обернутый в тег HTML <pre></pre>
    """
    log_list = []
    with open('log_file.txt', "r") as file:
        for log in file.readlines():

            log_list.append(log)

    return "<pre>" + "\n".join(log_list) + "</pre>"


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=3000)
