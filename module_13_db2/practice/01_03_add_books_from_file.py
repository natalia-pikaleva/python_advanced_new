import sqlite3

response = """
INSERT INTO table_books (ISBN, book_name, author, publish_year) VALUES (?, ?, ?, ?)
"""


def add_books_from_file(c: sqlite3.Cursor, file_name: str) -> None:
    with open(file_name, 'r') as file:
        for line in file.readlines()[1:]:
            book_info = tuple(line[:-1].split(','))
            c.execute(response, book_info)


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_books_from_file(cursor, "book_list.csv")
        conn.commit()
