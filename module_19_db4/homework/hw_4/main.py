import sqlite3

if __name__ == "__main__":
    with sqlite3.connect('../../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        response = """
        WITH all_assignments_students AS (
                SELECT a.group_id AS group_id, 
                        a.assisgnment_id AS assisgnment_id, 
                        a.due_date AS due_date, 
                        s.student_id AS student_id 
                FROM assignments a 
            
                INNER JOIN students s ON a.group_id = s.group_id
                ),
            overdue_assignments AS (
                SELECT aas.group_id AS group_id, aas.assisgnment_id AS assisgnment_id, aas.student_id AS student_id
                FROM all_assignments_students aas
                LEFT JOIN assignments_grades ag ON aas.assisgnment_id = ag.assisgnment_id AND aas.student_id = ag.student_id
                WHERE ag.date > aas.due_date OR ag.date IS NULL
                ORDER BY aas.group_id, aas.assisgnment_id
                ),
            task_counts AS (		
                SELECT group_id, assisgnment_id, COUNT(student_id) AS count_unfinish_tasks
                FROM overdue_assignments
                GROUP BY group_id, assisgnment_id
                )
            SELECT group_id, 
                MAX(count_unfinish_tasks) AS Max_tasks, 
                MIN(count_unfinish_tasks) AS Min_tasks, 
                ROUND(AVG(count_unfinish_tasks), 0) AS Average_tasks
            FROM task_counts
            GROUP BY group_id;
        """

        cursor.execute(response)

        result = cursor.fetchall()

        print('Список групп и количество просроченных заданий: максимальное, минимальное, среднее:')

        for index in range(len(result)):
            print(result[index])
