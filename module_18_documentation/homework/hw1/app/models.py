import sqlite3
from dataclasses import dataclass
from typing import Optional, Union, List, Dict

DATA = [
    {'id': 0, 'title': 'Властелин колец', 'author_first_name': 'Джон', 'author_last_name': 'Толкин',
     'author_middle_name': ''},
    {'id': 1, 'title': 'Гордость и предубеждение', 'author_first_name': 'Джейн', 'author_last_name': 'Остин',
     'author_middle_name': ''},
    {'id': 3, 'title': 'Гарри Поттер и Кубок огня', 'author_first_name': 'Джоан', 'author_last_name': 'Роулинг',
     'author_middle_name': ''},
]

DATABASE_NAME = 'table_books.db'
BOOKS_TABLE_NAME = 'books'
AUTHORS_TABLE_NAME = 'authors'


@dataclass
class Author:
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


@dataclass
class Book:
    title: str
    author: Author
    id: Optional[int] = None

    def __getitem__(self, item: str) -> Union[int, str]:
        return getattr(self, item)


def init_db(initial_records: List[Dict]) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='{BOOKS_TABLE_NAME}';
            """
        )
        exists = cursor.fetchone()
        if not exists:
            cursor.executescript(
                f"""
                CREATE TABLE `{AUTHORS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    middle_name TEXT DEFAULT '',
                    UNIQUE (last_name, first_name, middle_name)
                );
                """
            )

            cursor.executescript(
                f"""
                CREATE TABLE `{BOOKS_TABLE_NAME}`(
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    title TEXT,
                    author_id INTEGER,
                    FOREIGN KEY (author_id) REFERENCES "{AUTHORS_TABLE_NAME}"(id) ON DELETE CASCADE
                );
                """
            )
            cursor.executemany(
                f"""
                INSERT INTO `{AUTHORS_TABLE_NAME}`
                (first_name, last_name, middle_name) VALUES (?, ?, ?)
                ON CONFLICT(last_name, first_name, middle_name) DO NOTHING
                """,
                [(item['author_first_name'], item['author_last_name'], item['author_middle_name'])
                 for item in initial_records
                 ]
            )
            conn.commit()

            for item in initial_records:
                cursor.execute(f"""SELECT id FROM '{AUTHORS_TABLE_NAME}'
                                WHERE first_name = ? AND last_name = ? AND middle_name = ?
                                """, (item['author_first_name'], item['author_last_name'], item['author_middle_name']))

                author_id = cursor.fetchone()[0]

                cursor.execute(
                    f"""
                    INSERT INTO `{BOOKS_TABLE_NAME}`
                    (title, author_id) VALUES (?, ?)
                    """, (item['title'], author_id)
                )


def _get_book_obj_from_row(row: tuple) -> Book:
    return Book(id=row[0],
                title=row[1],
                author=Author(
                    id=row[2],  # Передаем ID автора
                    first_name=row[3],
                    last_name=row[4],
                    middle_name=row[5]
                ))


def get_all_books() -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT bt.id, bt.title, at.id, at.first_name, at.last_name, at.middle_name '
                       f'FROM "{BOOKS_TABLE_NAME}" bt '
                       f'JOIN "{AUTHORS_TABLE_NAME}" at ON bt.author_id = at.id')
        all_books = cursor.fetchall()

        return [_get_book_obj_from_row(row) for row in all_books]


def add_book(book: Book) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""SELECT id FROM `{AUTHORS_TABLE_NAME}`
                       WHERE first_name = ? AND last_name = ? AND (middle_name = ? OR middle_name IS NULL)
                    """,
            (book.author.first_name, book.author.last_name, book.author.middle_name or "")
        )

        author_row = cursor.fetchone()

        if author_row:
            author_id = author_row[0]
        else:
            add_author(book.author)
            author_id = cursor.lastrowid

        cursor.execute(
            f"""
                    INSERT INTO `{BOOKS_TABLE_NAME}`
                    (title, author_id) VALUES (?, ?)
                    """,
            (book.title, author_id)
        )

        book.id = cursor.lastrowid

        conn.commit()
    return book


def get_book_by_id(book_id: int) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
                    SELECT bt.id AS book_id, bt.title, 
                           at.id AS author_id, at.first_name, at.last_name, at.middle_name
                    FROM "{BOOKS_TABLE_NAME}" bt
                    JOIN "{AUTHORS_TABLE_NAME}" at ON bt.author_id = at.id
                    WHERE bt.id = ?
                    """,
            (book_id,)
        )
        row = cursor.fetchone()
        if row:
            return _get_book_obj_from_row(row)
    return None


def update_book_by_id(book: Book, book_id) -> Book:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE `{BOOKS_TABLE_NAME}` 
            SET title = ? 
            WHERE id = ?
            """,
            (book.title, book_id)
        )
        cursor.execute(
            f"""
                    UPDATE `{AUTHORS_TABLE_NAME}` 
                    SET first_name = ?, last_name = ?, middle_name = ? 
                    WHERE id = (SELECT author_id FROM `{BOOKS_TABLE_NAME}` WHERE id = ?)
                    """,
            (book.author.first_name, book.author.last_name, book.author.middle_name or "", book_id)
        )
        conn.commit()
    return book


def delete_book_by_id(book_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {BOOKS_TABLE_NAME}
            WHERE id = ?
            """,
            (book_id,)
        )
        conn.commit()
        return True


def get_book_by_title(book_title: str) -> Optional[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            SELECT bt.id, bt.title, at.id, at.first_name, at.last_name, at.middle_name 
            FROM '{BOOKS_TABLE_NAME}' bt
            JOIN '{AUTHORS_TABLE_NAME}' at 
            WHERE bt.title = ?
            """,
            (book_title,)
        )
        book = cursor.fetchone()
        if book:
            return _get_book_obj_from_row(book)


def _get_author_obj_from_row(row: tuple) -> Author:
    return Author(id=row[0],
                  first_name=row[1],
                  last_name=row[2],
                  middle_name=row[3]
                  )


def get_all_authors() -> list[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT id, first_name, last_name, middle_name '
                       f'FROM "{AUTHORS_TABLE_NAME}"')
        all_authors = cursor.fetchall()

        return [_get_author_obj_from_row(row) for row in all_authors]


def get_author_by_id(author_id: int) -> Optional[Author]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
                    SELECT id, first_name, last_name, middle_name
                    FROM "{AUTHORS_TABLE_NAME}"
                    WHERE id = ?
                    """,
            (author_id,)
        )
        row = cursor.fetchone()
        if row:
            return _get_author_obj_from_row(row)
    return None


def add_author(author: Author) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"""
                    INSERT INTO `{AUTHORS_TABLE_NAME}`
                    (first_name, last_name, middle_name) 
                    VALUES (?, ?, ?)
                    """,
            (author.first_name, author.last_name, author.middle_name or "")
        )
        author_id = cursor.lastrowid
        author.id = author_id
        conn.commit()
    return author


def get_all_books_of_author(author: Author) -> list[Book]:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT bt.id, bt.title, at.id, at.first_name, at.last_name, at.middle_name '
                       f'FROM "{BOOKS_TABLE_NAME}" bt '
                       f'JOIN "{AUTHORS_TABLE_NAME}" at ON bt.author_id = at.id '
                       f'WHERE at.first_name = ? AND at.last_name = ? AND at.middle_name = ? ',
                       (author.first_name, author.last_name, author.middle_name or ""))
        all_books_of_author = cursor.fetchall()

        return [_get_book_obj_from_row(row) for row in all_books_of_author]


def delete_author_by_id(author_id: int) -> None:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            DELETE FROM {AUTHORS_TABLE_NAME}
            WHERE id = ?
            """,
            (author_id,)
        )
        cursor.execute(
            f"""
                    DELETE FROM {BOOKS_TABLE_NAME}
                    WHERE author_id = ?
                    """,
            (author_id,)
        )
        conn.commit()
        return True


def update_author_by_id(author: Author, author_id: int) -> Author:
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"""
            UPDATE `{AUTHORS_TABLE_NAME}` 
            SET first_name = ?, last_name = ?, middle_name = ?
            WHERE id = ?
            """,
            (author.first_name, author.last_name, author.middle_name, author_id)
        )

        conn.commit()
    return author
