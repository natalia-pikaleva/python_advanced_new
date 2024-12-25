import datetime
from flask import Flask

app = Flask(__name__)
count = 0

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