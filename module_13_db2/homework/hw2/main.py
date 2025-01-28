import sqlite3


def delete_wrong_fees(
        cursor: sqlite3.Cursor,
        wrong_fees_file: str
) -> None:
    response = """
    DELETE FROM table_fees
        WHERE truck_number = ? AND timestamp = ?
    """

    with open(wrong_fees_file, 'r') as file:
        for line in file.readlines():
            cursor.execute(response, tuple(line[:-1].split(',')))


if __name__ == "__main__":
    with sqlite3.connect("../homework.db") as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, "../wrong_fees.csv")
        conn.commit()
