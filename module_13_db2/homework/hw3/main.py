from datetime import datetime, timezone
import sqlite3


def generate_table(cursor: sqlite3.Cursor) -> None:
    try:
        response = """
            CREATE TABLE IF NOT EXISTS `table_birds` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp VARCHAR(100) NOT NULL,
                name VARCHAR(100)
            );
            """
        cursor.executescript(response)


    except sqlite3.Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def log_bird(
        cursor: sqlite3.Cursor,
        bird_name: str,
        date_time: str,
) -> None:
    response = """
    INSERT INTO table_birds (timestamp, name) VALUES (?, ?)
    """

    cursor.execute(response, (date_time, bird_name))


def check_if_such_bird_already_seen(
        cursor: sqlite3.Cursor,
        bird_name: str
) -> bool:
    response = """
    SELECT * FROM table_birds WHERE name = ?
    """

    cursor.execute(response, (bird_name,))

    result = cursor.fetchall()

    if result:
        return True

    return False


if __name__ == "__main__":
    print("Программа помощи ЮНатам v0.1")
    name: str = input("Пожалуйста введите имя птицы\n> ")
    count_str: str = input("Сколько птиц вы увидели?\n> ")
    count: int = int(count_str)
    right_now: str = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect("../homework.db") as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        generate_table(cursor)
        if check_if_such_bird_already_seen(cursor, name):
            print("Такую птицу мы уже наблюдали!")

        log_bird(cursor, name, right_now)
