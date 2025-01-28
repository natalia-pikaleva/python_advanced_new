import sqlite3


def ivan_sovin_the_most_effective(
        cursor: sqlite3.Cursor,
        name: str,
) -> None:
    response_salary_Sovin = """
    SELECT salary FROM table_effective_manager WHERE name = "Иван Совин"
    """
    cursor.execute(response_salary_Sovin)
    SOVIN_SALARY, *_ = cursor.fetchone()

    response_delete_people = """
        DELETE FROM table_effective_manager
            WHERE name = ? AND ROUND(salary * 1.1, 0) >= ?
        """
    cursor.execute(response_delete_people, (name, SOVIN_SALARY))

    response_update_salary = """
        UPDATE table_effective_manager
            SET salary = ROUND(salary * 1.1, 0)
            WHERE name = ? AND ROUND(salary * 1.1, 0) < ?;
        """
    cursor.execute(response_update_salary, (name, SOVIN_SALARY))


if __name__ == '__main__':
    # name: str = input('Введите имя сотрудника: ')
    name = 'Степанов Л.Ч.'
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_sovin_the_most_effective(cursor, name)
        conn.commit()
