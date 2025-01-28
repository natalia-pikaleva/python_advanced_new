import sqlite3


def get_number_of_lucky_days(c: sqlite3.Cursor, month_number: int) -> float:
    response = """
            WITH lucky_days AS (
                SELECT DISTINCT date
                FROM table_green_future
                WHERE date LIKE ?
                GROUP BY date
                HAVING
                    COUNT(CASE WHEN action = 'мешок пластика' THEN 1 END) >= 2
                    AND COUNT(CASE WHEN action = 'мешок алюминия' THEN 1 END) >= 1
                    AND COUNT(CASE WHEN action = 'отнесли мешки на завод' THEN 1 END) >= 1
            ),
            total_days AS (
                SELECT COUNT(DISTINCT date) AS total
                FROM table_green_future
                WHERE date LIKE ?
            )
            SELECT (COUNT(*) * 100.0) / (SELECT total FROM total_days)
            FROM lucky_days;
            """

    pattern = f'%-{str(month_number).zfill(2)}-%'
    c.execute(response, (pattern, pattern))

    result, *_ = c.fetchone()

    return result


if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        percent_of_lucky_days = get_number_of_lucky_days(cursor, 12)
        print(f"В декабре у ребят было {percent_of_lucky_days:.02f}% удачных дня!")
