import logging
import os
import time
import threading
from typing import List
import json
from pprint import pprint
import sqlite3
from multiprocessing.pool import ThreadPool
import multiprocessing

import requests

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)

URL: str = 'https://www.swapi.tech/api/people/'

ID_NUMBERS = [id for id in range(1, 21)]


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


def get_people(id: int) -> None:
    id_url = URL + str(id)
    response: requests.Response = requests.get(id_url, timeout=(5, 5))

    if response.status_code != 200:
        return
    try:
        data = response.json()

        name = data['result']['properties']['name']
        birth_year = data['result']['properties']['birth_year']
        gender = data['result']['properties']['gender']
        conn = create_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO star_wars_people (name, birth_year, gender) VALUES (?, ?, ?)",
                       (name, birth_year, gender))
        except sqlite3.OperationalError:
            initialize_db()
            cursor.execute("INSERT INTO star_wars_people (name, birth_year, gender) VALUES (?, ?, ?)",
                           (name, birth_year, gender))

        conn.commit()
        conn.close()

    except ValueError as e:
        print(f"Ошибка при разборе JSON: {e}")


def load_people_sequential() -> None:
    start: float = time.time()
    for id in range(1, 21):
        get_people(id)
    end = time.time()
    logger.info(f'Time taken in seconds for sequential - {end - start}')


def get_people_with_processpool():
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    start = time.time()
    result = pool.map(get_people, ID_NUMBERS)
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f'Time taken in seconds with processes pool - {end - start}')


def load_people_with_threadpool():
    pool = ThreadPool(processes=multiprocessing.cpu_count() * 20)
    start = time.time()
    result = pool.map(get_people, ID_NUMBERS)
    pool.close()
    pool.join()
    end = time.time()
    logger.info(f'Time taken in seconds with threadpool - {end - start}')


if __name__ == '__main__':
    # load_people_sequential()

    get_people_with_processpool()

    load_people_with_threadpool()