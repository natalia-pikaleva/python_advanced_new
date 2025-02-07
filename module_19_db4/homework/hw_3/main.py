import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        # Запрос с вложенными запросами
        response = """
        SELECT s.full_name
            FROM students s
            WHERE s.group_id IN (
                SELECT sg.group_id
                FROM students_groups sg
                WHERE sg.teacher_id IN (
                    SELECT a.teacher_id
                    FROM assignments_grades ag
                    JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
                    GROUP BY a.teacher_id
                    ORDER BY AVG(ag.grade) DESC
                    LIMIT 1
                )
            );
        """

        # Другой вариант того же запроса

        # response = """
        # WITH best_teacher AS (
        #     SELECT a.teacher_id, AVG(ag.grade) AS average_grade
        #     FROM assignments_grades ag
        #     JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
        #     GROUP BY a.teacher_id
        #     ORDER BY average_grade DESC
        #     LIMIT 1
        #     ),
        #
        #     groups_of_best_teacher AS (
        #         SELECT sg.group_id AS group_id FROM students_groups sg
        #         JOIN best_teacher bt
        #         ON sg.teacher_id = bt.teacher_id
        #     )
        # SELECT s.full_name FROM students s
        #     JOIN groups_of_best_teacher gbt
        #     ON s.group_id = gbt.group_id;
        # """

        cursor.execute(response)

        result = cursor.fetchall()

        print('Список студентов преподавателя, у которого самые простые задания:')

        for index in range(len(result)):
            print(result[index][0])
