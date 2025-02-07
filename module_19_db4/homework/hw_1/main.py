import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        response = """
        WITH low_avg_grade AS (
            SELECT a.teacher_id, AVG(ag.grade) AS average_grade
            FROM assignments_grades ag
            JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
            GROUP BY a.teacher_id
            ORDER BY average_grade ASC
            LIMIT 1
                )
        SELECT t.full_name
            FROM teachers t
            JOIN low_avg_grade lag ON t.teacher_id = lag.teacher_id;
        """

        cursor.execute(response)

        result, *_ = cursor.fetchone()

        print(f'Преподаватель {result} задает самые сложные задания')
