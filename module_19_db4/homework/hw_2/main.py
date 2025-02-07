import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        response = """
        WITH best_students AS (
            SELECT 
                ag.student_id,
                AVG(ag.grade) AS average_grade
            FROM assignments_grades ag
            JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
            GROUP BY ag.student_id
            ORDER BY average_grade DESC 
            LIMIT 10
                 )
        SELECT s.full_name
            FROM students s
            JOIN best_students bs ON s.student_id = bs.student_id
        """

        cursor.execute(response)

        result = cursor.fetchall()

        print('Список лучших студентов:')

        for index in range(len(result)):
            print(result[index][0])
