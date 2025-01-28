import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('practise.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT COUNT(wind) FROM table_kotlin WHERE wind >= 33
        """)

        result, *_ = cursor.fetchone()

        print(f'Количество дней с ураганным ветром было: {result}')