"""
Напишите эндпоинт, который принимает на вход код на Python (строка)
и тайм-аут в секундах (положительное число не больше 30).
Пользователю возвращается результат работы программы, а если время, отведённое на выполнение кода, истекло,
то процесс завершается, после чего отправляется сообщение о том, что исполнение кода не уложилось в данное время.
"""
import shlex
import subprocess

from flask import Flask, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, NumberRange
from time import sleep

app = Flask(__name__)


class CodeForm(FlaskForm):
    code = StringField(validators=[InputRequired()])
    timeout = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=30)])


def run_python_code_in_subproccess(code: str, timeout: int):
    comand = ['python', '-c', code]

    process = subprocess.Popen(comand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        raise Exception("Process timed out")

    return stdout.decode('utf-8'), stderr.decode('utf-8'), process.returncode

@app.route('/run_code', methods=['POST'])
def run_code():
    form = CodeForm()

    if form.validate_on_submit():
        code = form.code.data
        timeout = form.timeout.data

        try:
            output, error, returncode = run_python_code_in_subproccess(code, timeout)


            if returncode != 0 or error:
                return jsonify({"error": error.strip()}), 400

            return jsonify({"output": output.strip()})

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    return f'Invalid input, {form.errors}', 400



if __name__ == '__main__':
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)
