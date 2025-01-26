from datetime import datetime
import time
from flask import Flask
import threading
import requests
from queue import Queue

app: Flask = Flask(__name__)


@app.route('/timestamp/<timestamp>')
def get_timestamp(timestamp: str) -> str:
    timestamp: float = float(timestamp)
    return str(datetime.fromtimestamp(timestamp))


def thread_function(log_queue, id_thread):
    current_timestamp = int(time.time())

    for i in range(20):
        time.sleep(1)
        response = requests.get(f'http://127.0.0.1:8080/timestamp/{current_timestamp}')
        log_entry = f'{current_timestamp} {response.text}'
        log_queue.put(log_entry)
        current_timestamp += 1


def main():
    log_queue = Queue()
    threads = []

    for i in range(10):
        thread = threading.Thread(target=thread_function, args=(log_queue, i))
        threads.append(thread)
        thread.start()
        time.sleep(1)

    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())

    with open('logs.txt', 'w') as log_file:
        for log in logs:
            log_file.write(log + '\n')


if __name__ == '__main__':
    threading.Thread(target=app.run,
                     kwargs={'host': '127.0.0.1', 'port': 8080}).start()
    main()
