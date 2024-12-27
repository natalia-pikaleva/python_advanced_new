import random
from datetime import datetime, timedelta
import re
import os

from flask import Flask

CARS_LIST = ['Chevrolet', 'Renault', 'Ford', 'Lada']
CATS_LIST = ['корниш-рекс', "русская голубая", "шотландская вислоухая", "мейн-кун", "манчкин"]

BASE_DIR = 'C:\\Users\\deva0\\PycharmProjects\\python_advanced\\module_01_flask\\homework'
BOOK_FILE = os.path.join(BASE_DIR, 'war_and_peace.txt')

app = Flask(__name__)



text_of_book = ''
with open(BOOK_FILE, 'r', encoding='utf8') as file:
    for i_line in file:
        text_of_book += i_line

words = re.findall(r'\w+', text_of_book)

@app.route('/test')
def test_function():
    now = datetime.datetime.now().utcnow()
    return f'Это новая тестовая страничка, ответ сгенерирован в {now}'


@app.route('/hello_world')
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
    count = 0


    app.run(debug=True)