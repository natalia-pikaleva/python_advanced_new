import logging
import os
import time
import threading
from typing import List
import json
from pprint import pprint
import sqlite3

import requests

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

URL: str = 'https://www.swapi.tech/api/people/'


def create_connection():
    return sqlite3.connect('star_wars_database.db')


def initialize_db():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS star_wars_people (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        birth_year TEXT,
        gender TEXT
    )
    ''')
    conn.commit()
    conn.close()


def get_people(url: str, id: int) -> None:
    response: requests.Response = requests.get(url, timeout=(5, 5))

    if response.status_code != 200:
        return
    try:
        data = response.json()

        name = data['result']['properties']['name']
        birth_year = data['result']['properties']['birth_year']
        gender = data['result']['properties']['gender']
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO star_wars_people (name, birth_year, gender) VALUES (?, ?, ?)",
                       (name, birth_year, gender))
        conn.commit()
        conn.close()

    except ValueError as e:
        print(f"Ошибка при разборе JSON: {e}")


def load_people_sequential() -> None:
    start: float = time.time()
    for id in range(1, 21):
        i_URL = URL + str(id)
        get_people(i_URL, id)
    logger.info('Done in {:.4}'.format(time.time() - start))


def load_people_multithreading() -> None:
    start: float = time.time()
    threads: List[threading.Thread] = []
    for i in range(1, 21):
        thread = threading.Thread(target=get_people, args=(URL + str(i), i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.info('Done in {:.4}'.format(time.time() - start))


if __name__ == '__main__':
    load_people_sequential()

    load_people_multithreading()
