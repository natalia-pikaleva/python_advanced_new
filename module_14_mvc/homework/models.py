import sqlite3
from typing import Any, Optional, List

DATA: List[dict] = [
    {'id': 0, 'title': 'A Byte of Python', 'author': 'Swaroop C. H.'},
    {'id': 1, 'title': 'Moby-Dick; or, The Whale', 'author': 'Herman Melville'},
    {'id': 3, 'title': 'War and Peace', 'author': 'Leo Tolstoy'},
]


class Book:

    def __init__(self, id: int, title: str, author: str, count_find: int = 0) -> None:
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.count_find: int = count_find

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_books'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_books` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                count_find INTEGER
                );
                """
                # TODO последнему полю достаточно указать значение по-умолчанию INTEGER DEFAULT 0 и тогда не пришлось
                #  бы в скрипте инкремента поля использовать IFNULL
            )
            cursor.executemany(
                """
                INSERT INTO `table_books`
                (title, author) VALUES (?, ?)
                """,
                [
                    (item['title'], item['author'])
                    for item in initial_records
                ]
            )


def get_all_books() -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_books`
            """
        )

        book_list = [Book(*row) for row in cursor.fetchall()]
        for i_book in book_list:
            response = """
                       UPDATE `table_books`
                           SET count_find = IFNULL(count_find, 0) + 1
                           WHERE id = ?
                       """
            # TODO как видите, данный код дублируется несколько раз, стоит вынести его в отдельную функцию, желательно
            #  универсальную, с параметром - списком id книг для инкремента просмотров (в запросе вместо where id =
            #  используйте where id in <id list>
            cursor.execute(response, (i_book.id,))
            cursor.connection.commit()

        return book_list


def get_books_of_author(author: str) -> List[Book]:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        response = """
            SELECT id, title, author from `table_books` WHERE author = ?
            """
        cursor.execute(response, (author,))
        book_list = [Book(*row) for row in cursor.fetchall()]
        for i_book in book_list:
            response = """
                                UPDATE `table_books`
                                    SET count_find = IFNULL(count_find, 0) + 1
                                    WHERE id = ?
                                """
            cursor.execute(response, (i_book.id,))
            cursor.connection.commit()

        return book_list


def get_count_books() -> int:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        cursor.execute("""
        SELECT COUNT(*) FROM `table_books`
        """)
        result, *_ = cursor.fetchone()
        return result


def add_book_in_db(title: str, author: str) -> None:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        response = """
        INSERT INTO `table_books` (title, author) VALUES (?, ?)
        """
        cursor.execute(response, (title, author))


def get_book_id(book_id: int) -> Book:
    with sqlite3.connect('table_books.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        response = """
                    UPDATE `table_books`
                        SET count_find = IFNULL(count_find, 0) + 1
                        WHERE id = ?
                    """
        cursor.execute(response, (book_id,))
        cursor.connection.commit()

        response = """
            SELECT * from `table_books` WHERE id = ?
            """
        cursor.execute(response, (book_id,))
        result = cursor.fetchone()
        if result:
            id, title, author, count_find = result

            return Book(id, title, author, count_find)
        return None
