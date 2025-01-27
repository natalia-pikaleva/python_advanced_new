import sqlite3


def add_10_records_to_table_warehouse(cursor: sqlite3.Cursor) -> None:
    response = """
    INSERT INTO 'table_warehouse' (name, description, amount) VALUES 
            (?, ?, ?)
    """

    DATA = [('вяленый томат', 'сорт вялаый томат', 500),
            ('вяленый персик', 'производство Абхазия', 1000),
            ('изюм', 'виноград сушеный', 1500),
            ('курага', 'прошлогодняя', 2000),
            ('чернослив', 'сливы сушеные', 1000),
            ('миндаль', 'жареный', 1000),
            ('фисташки', 'соленые в скорлупе', 1500),
            ('цукаты', 'производство Таиланд', 2000),
            ('арахис', 'неочищенный', 1300),
            ('фундук', 'новый урожай', 3000)]

    for item in DATA:
        cursor.execute(response, item)

if __name__ == "__main__":
    with sqlite3.connect("practise.db") as conn:
        cursor = conn.cursor()
        add_10_records_to_table_warehouse(cursor)
        conn.commit()
