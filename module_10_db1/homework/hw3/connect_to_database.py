import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_3_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT "
                       "(SELECT COUNT(*) FROM table_1) AS table1_count,"
                       "(SELECT COUNT(*) FROM table_2) AS table2_count,"
                       "(SELECT COUNT(*) FROM table_3) AS table3_count")

        result = cursor.fetchall()


        print('Количество строк в таблицах:')
        print(f'Таблица 1: {result[0][0]}, таблица 2: {result[0][1]}, таблица 3: {result[0][2]}')

        cursor.execute("SELECT COUNT(DISTINCT id) FROM table_1 AS unic_table1_count")

        result = cursor.fetchall()

        print(f'Количество уникальных записей в таблице 1: {result[0][0]}')

        cursor.execute("SELECT COUNT(DISTINCT t1.id) AS count_table1_in_table2 "
                       "FROM table_1 t1 JOIN table_2 t2 ON t1.id = t2.id")

        result = cursor.fetchall()

        print(f'Количество записей таблицы 1, которые есть в таблице 2: {result[0][0]}')

        cursor.execute("SELECT COUNT(DISTINCT t1.id) AS count_table1_in_table2_and_table3 "
                       "FROM table_1 t1 JOIN table_2 t2 ON t1.id = t2.id "
                       "JOIN table_3 t3 ON t1.id = t3.id")

        result = cursor.fetchall()

        print(f'Количество записей таблицы 1, которые есть в таблице 2 и в таблице 3: {result[0][0]}')

