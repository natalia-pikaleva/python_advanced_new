"""
Заменим сообщение "The requested URL was not found on the server" на что-то более информативное.
Например, выведем список всех доступных страниц с возможностью перехода по ним.

Создайте Flask Error Handler, который при отсутствии запрашиваемой страницы будет выводить
список всех доступных страниц на сайте с возможностью перехода на них.
"""

from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    available_routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static' and rule.endpoint != 'page_not_found':
            available_routes.append(rule)

    return render_template('404.html', available_routes=available_routes), 404

@app.route('/dogs')
def dogs():
    return 'Страница с пёсиками'


@app.route('/cats')
def cats():
    return 'Страница с котиками'


@app.route('/cats/<int:cat_id>')
def cat_page(cat_id: int):
    return f'Страница с котиком {cat_id}'


@app.route('/index')
def index():
    return 'Главная страница'


if __name__ == '__main__':
    app.run(debug=True)
