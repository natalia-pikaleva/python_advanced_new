import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_4_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT"
                       "(SELECT COUNT(*) FROM salaries WHERE salary < 5000) AS poverty_count,"
                       "(SELECT COUNT(*) FROM salaries) AS total_count")

        result = cursor.fetchall()

        print(f'Количество жителей за чертой бедности: {result[0][0]}, всего жителей: {result[0][1]}')

        cursor.execute("SELECT ROUND(AVG(salary), 2) FROM salaries")

        result = cursor.fetchall()

        print(f'Средняя заработная плата: {result[0][0]}')

        cursor.execute("SELECT AVG(val) AS median "
                       "FROM (SELECT salary AS val FROM salaries "
                       "ORDER BY salary LIMIT 2 OFFSET "
                       "(SELECT COUNT(*) FROM salaries) / 2) AS sub_query")

        result = cursor.fetchall()

        print(f'Медианная заработная плата: {result[0][0]}')

        cursor.execute("WITH "
                       "TotalCount AS (SELECT COUNT(salary) AS TotalCount FROM salaries), "
                       "SortedSalaries AS (SELECT salary FROM salaries ORDER BY salary DESC), "
                       "Top10percent AS (SELECT SUM(salary) AS X "
                       "FROM (SELECT salary FROM SortedSalaries "
                       "LIMIT CAST(0.1 * (SELECT TotalCount FROM TotalCount) AS INT)) AS TopSalaries), "
                       "Percent100 AS (SELECT SUM(salary) AS TotalSumSalaries FROM salaries), "
                       "Y_CTE AS (SELECT (TotalSumSalaries - X) AS Y FROM Percent100, Top10percent) "
                       "SELECT 100 * ROUND(CAST((SELECT X FROM Top10percent) AS FLOAT) / NULLIF((SELECT Y FROM Y_CTE), 0), 2) AS Result")


        result = cursor.fetchone()

        print(f'Число социального неравенства: {result[0]}%')
