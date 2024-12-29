"""
Реализуйте endpoint /hello-world/<имя>, который возвращает строку «Привет, <имя>. Хорошей пятницы!».
Вместо хорошей пятницы endpoint должен уметь желать хорошего дня недели в целом, на русском языке.

Пример запроса, сделанного в субботу:

/hello-world/Саша  →  Привет, Саша. Хорошей субботы!
"""

from flask import Flask
from datetime import datetime
import sys

app = Flask(__name__)


@app.route('/hello-world/<name>')
def hello_world(name: str):
    '''
    Функция получает на входе имя пользователя name и возвращает фразу согласно условиям задачи
    :param name: имя пользователя
    :return: фраза согласно условиям задачи
    '''

    weekday = weekdays_tuple[datetime.today().weekday()]
    return f'Привет, {name}. {weekday}!'


if __name__ == '__main__':
    weekdays_tuple = ('Хорошего понедельника', 'Хорошего вторника', 'Хорошей среды', 'Хорошего четверга', 'Хорошей пятницы', 'Хорошей субботу', 'Хорошего воскресенья')

    app.run(debug=True)