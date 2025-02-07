import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        # номер группы, количество студентов, средняя оценка, количество студентов, не сдавших хотя бы одно задание,
        # количество студентов, кто сдал задание позже срока
        response = """
        WITH repeated_assignments AS (
            SELECT assisgnment_id, student_id, COUNT(*) AS repeat_count
            FROM assignments_grades ag 
            GROUP BY assisgnment_id, student_id 
            HAVING COUNT(*) > 1
        ),
        overdue_tasks AS (
            SELECT a.group_id, COUNT(DISTINCT ag.student_id) AS Overdue_task_students
            FROM assignments a 
            JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id 
            WHERE ag.date > a.due_date 
            GROUP BY a.group_id
        )
        SELECT
            s.group_id,
            ROUND(AVG(ag.grade), 2) AS Average_grade,
            COUNT(DISTINCT s.student_id) AS Count_students,
            COUNT(DISTINCT CASE WHEN ag_outer.grade IS NULL THEN s.student_id END) AS Count_not_complete_student,
            COALESCE(ot.Overdue_task_students, 0) AS Overdue_task_students,
            COUNT(DISTINCT ra.student_id) AS Repeated_task_students
        FROM
            students s
        JOIN
            assignments_grades ag ON ag.student_id = s.student_id
        LEFT JOIN assignments a ON a.group_id = s.group_id
        LEFT JOIN assignments_grades ag_outer ON a.assisgnment_id = ag_outer.assisgnment_id AND s.student_id = ag_outer.student_id
        LEFT JOIN overdue_tasks ot ON s.group_id = ot.group_id
        LEFT JOIN repeated_assignments ra ON s.student_id = ra.student_id
        GROUP BY
            s.group_id;


        """

        cursor.execute(response)

        result = cursor.fetchall()

        print('Список групп и информация по каждой группе: средняя оценка, \n'
              'общее количество учеников, количество учеников, которые не сдали работы, \n'
              'количество учеников, которые просрочили дедлайн, \n'
              'количество повторных попыток сдать работу:')

        for index in range(len(result)):
            print(result[index])
