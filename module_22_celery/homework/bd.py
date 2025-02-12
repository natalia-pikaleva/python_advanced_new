import sqlite3
from celery import Celery

celery = Celery('app',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')


@celery.task
def save_data_ib_bd(email, files_list):
    with sqlite3.connect('orders_bd') as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='blur_orders';
        """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `blur_orders`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    file_name TEXT NOT NULL
                );
                """
            )

        conn.commit()

        response_insert = """
        INSERT INTO blur_orders(email, file_name) VALUES (?, ?)
        """
        for file_name in files_list:
            cursor.execute(response_insert, (email, file_name))
        conn.commit()


@celery.task
def get_data_by_email(email):
    with sqlite3.connect('orders_bd') as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"""
        SELECT id, file_name FROM blur_orders 
        WHERE email = ?;
        """, (email,)
        )
        if cursor.fetchone():
            id, file_name, *_ = cursor.fetchone()
        else:
            id = '1'
            file_name = ''

        return id, file_name
