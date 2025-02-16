import time
import random

from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)


@app.route('/one')
@metrics.counter(
    'one_count', 'Number of invocations',
    labels={'status': lambda resp: resp.status_code}
)
def first_route():
    time.sleep(random.random() * 2)
    return 'ok'


@app.route('/two')
@metrics.counter(
    'two_count', 'Number of invocations',
    labels={'status': lambda resp: resp.status_code}
)
def the_second():
    time.sleep(random.random() * 4)
    return 'ok'


@app.route('/three')
@metrics.counter(
    'three_count', 'Number of invocations',
    labels={'status': lambda resp: resp.status_code}
)
def test_3rd():
    time.sleep(random.random() * 6)
    return 'ok'


@app.route('/four')
@metrics.counter(
    'four_count', 'Number of invocations',
    labels={'status': lambda resp: resp.status_code}
)
def fourth_one():
    time.sleep(random.random() * 8)
    return 'ok'


@app.route('/error')
@metrics.counter(
    'error_count', 'Number of invocations',
    labels={'status': lambda resp: resp.status_code}
)
def oops():
    return ':(', 500


if __name__ == '__main__':
    app.run('0.0.0.0', 5000, threaded=True)
