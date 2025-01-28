import sqlite3

from datetime import datetime, timedelta

SECTION = ['футбол', 'хоккей', 'шахматы', 'SUP-сёрфинг', 'бокс', 'Dota2', 'шахбокс']


def date_generator(start, end):
    while start <= end:
        yield start
        start += timedelta(days=1)


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    response_delete_table = """
    DELETE FROM `table_friendship_schedule`
    """

    cursor.execute(response_delete_table)

    start_date = datetime.strptime('2020-01-01', '%Y-%m-%d')
    end_date = datetime.strptime('2020-12-31', '%Y-%m-%d')

    response_get_ids_first = """
    SELECT id FROM table_friendship_employees tfe 
    WHERE NOT preferable_sport = ? AND
        id NOT IN (
            SELECT employee_id FROM table_friendship_schedule tfs 
        )
    LIMIT ?;
    """

    response_get_ids_other = """
    SELECT id
        FROM table_friendship_employees tfe
        WHERE NOT preferable_sport = ?
        AND 
        id IN (
            SELECT employee_id
            FROM table_friendship_schedule tfs
            GROUP BY employee_id
            HAVING COUNT(employee_id) <= ?
            ) 
    LIMIT ?
    """

    response_insert_for_table = """
    INSERT INTO `table_friendship_schedule` (employee_id, date) VALUES (?, ?)
    """

    count_of_working_shifts = 0  # количество смен каждого сотрудника, изначально 0

    for date in date_generator(start_date, end_date):
        # определяем хобби в эту дату
        day_number = date.weekday()
        hobby = SECTION[day_number]

        if count_of_working_shifts == 0:

            # первый раз заполняем таблицу id сотрудников, распределяем по 1 смене
            cursor.execute(response_get_ids_first, (hobby, 10))
            result = cursor.fetchall()
            ids_for_date = tuple(item[0] for item in result)

            for id in ids_for_date:
                cursor.execute(response_insert_for_table, (id, str(date)))

            count_ids = len(ids_for_date)

            # не хватило id сотрудников, чтобы заполнить всю смену, заполняем смену
            # id сотрудниками, у которых уже есть 1 смена
            if count_ids < 10:
                count_of_working_shifts += 1
                cursor.execute(response_get_ids_other, (hobby, count_of_working_shifts, 10 - count_ids))
                result = cursor.fetchall()
                ids_for_date = tuple(item[0] for item in result)

                for id in ids_for_date:
                    cursor.execute(response_insert_for_table, (id, str(date)))

        else:
            cursor.execute(response_get_ids_other, (hobby, count_of_working_shifts, 10))
            result = cursor.fetchall()
            ids_for_date = tuple(item[0] for item in result)

            for id in ids_for_date:
                cursor.execute(response_insert_for_table, (id, str(date)))

            count_ids = len(ids_for_date)

            if count_ids < 10:  # не хватило id сотрудников, чтобы заполнить всю смену
                cursor.execute(response_get_ids_other, (hobby, count_of_working_shifts, 10 - count_ids))
                result = cursor.fetchall()
                ids_for_date = tuple(item[0] for item in result)

                for id in ids_for_date:
                    cursor.execute(response_insert_for_table, (id, str(date)))

                count_of_working_shifts += 1


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
