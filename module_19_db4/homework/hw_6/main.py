import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        response = """
        SELECT ROUND(AVG(ag.grade), 2) AS Average_grade
            FROM assignments_grades ag 
            WHERE ag.assisgnment_id IN (
                    SELECT a.assisgnment_id AS assisgnment_id
                    FROM assignments a 
                    WHERE a.assignment_text LIKE '%прочитать%' OR a.assignment_text LIKE '%выучить%'
                    )
        """

        cursor.execute(response)

        result, *_ = cursor.fetchone()

        print(f'Средняя оценка за задания, в которых нужно что-то прочитать или выучить: {result}')
