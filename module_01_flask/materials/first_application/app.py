import random
from datetime import datetime, timedelta
import re
import os

from flask import Flask

app = Flask(__name__)

count = 0  # TODO основной код программы должен располагаться после определения всех функций

cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']
cats_list = ['корниш-рекс', "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]
# TODO сделайте эти переменные константами (имя констант пишется прописными буквами, а располагаются константы в начале
#  модуля, сразу после импортов). За одно помечать константы как global в функциях не придется

BASE_DIR = 'C:\\Users\\deva0\\PycharmProjects\\python_advanced\\module_01_flask\\homework'
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')
# TODO расположите константы в начале модуля, сразу после импортов

text_of_book = ''

with open(BOOK_FILE, 'r', encoding='utf8') as file:
    for i_line in file:
        text_of_book += i_line

words = re.findall(r'\w+', text_of_book)
# TODO этот код выше (включая text_of_book = '') тоже основной код программы - должен распологаться после определения
#  всех функций

@app.route('/test')
def test_function():
    now = datetime.datetime.now().utcnow()
    return f'Это новая тестовая страничка, ответ сгенерирован в {now}'

@app.route('/hello_world')  # TODO Определение функции должно отделяться от остального кода двумя пустыми строками
def hello_world():
    return 'Hello, world!'

@app.route('/counter')
def counter():
    global count
    count += 1
    return str(count)

@app.route('/cars')
def cars():
    global cars_list
    return ', '.join(cars_list)

@app.route('/cats')
def cats():
    global cats_list
    random_cat = random.choice(cats_list)
    return random_cat

@app.route('/get_time/now')
def get_time_now():
    current_time = datetime.now()
    return 'Точное время: {}'.format(current_time)

@app.route('/get_time/future')
def get_time_future():
    current_time_after_hour = datetime.now() + timedelta(hours=1)
    return 'Точное время через час будет: {}'.format(current_time_after_hour)

@app.route('/get_random_word')
def get_random_word():
    global words
    random_word = random.choice(words)

    return 'Случайное слово из книги Война и мир: {}'.format(random_word)


if __name__ == '__main__':
    app.run(debug=True)