import random
import sqlite3


def generate_test_data(
        cursor: sqlite3.Cursor,
        number_of_groups: int
) -> None:
    response = """
    INSERT INTO uefa_commands (command_number, command_name, command_country, command_level) VALUES (?, ?, ?, ?)
    """

    NAME_COMMANDS = ['Зенит', 'Реал Мадрид', 'Барселона', 'Спартак',
                     'Краснодар', 'ЦСКА', 'Локомотив', 'Манчестер Юнайтед',
                     'Ливерпуль', 'Манчестер Сити', 'Челси', 'Рубин',
                     'Бавария', 'Реал Сосьедад', 'Ювентус', 'Арсенал']
    COUNTRYES = ['Россия', 'Испания', 'Аргентина', 'Великобритания', 'Германия']

    for command_number in range(1, number_of_groups + 1):
        command_name = NAME_COMMANDS[command_number - 1]
        command_country = random.choice(COUNTRYES)
        command_level = random.randint(1, 8)
        cursor.execute(response, (command_number, command_name, command_country, command_level))

    response_high_level = """
    SELECT command_number FROM uefa_commands ORDER BY command_level DESC LIMIT ?
    """

    count_groups = number_of_groups // 4
    cursor.execute(response_high_level, (count_groups,))
    result = cursor.fetchall()
    high_level_command_numbers = tuple(item[0] for item in result)

    response_low_level = """
        SELECT command_number FROM uefa_commands ORDER BY command_level LIMIT ?
        """

    cursor.execute(response_low_level, (count_groups,))
    result = cursor.fetchall()
    low_level_command_numbers = tuple(item[0] for item in result)

    response_average_level = """
            WITH RankedData AS (
                SELECT 
                    command_number,
                    ROW_NUMBER() OVER (ORDER BY command_level ASC) as row_num_asc,
                    ROW_NUMBER() OVER (ORDER BY command_level DESC) as row_num_desc
                FROM uefa_commands
                )
                SELECT command_number
                FROM RankedData
                WHERE row_num_asc > ? AND row_num_desc > ?;
            """

    cursor.execute(response_average_level, (count_groups, count_groups))
    result = cursor.fetchall()
    average_level_command_numbers = tuple(item[0] for item in result)

    response_insert_commands = """
    INSERT INTO uefa_draw (command_number, group_number) VALUES (?, ?)
    """

    for group_number in range(1, count_groups + 1):
        cursor.execute(response_insert_commands, (high_level_command_numbers[group_number - 1], group_number))
        cursor.execute(response_insert_commands, (low_level_command_numbers[group_number - 1], group_number))
        cursor.execute(response_insert_commands, (average_level_command_numbers[(group_number - 1) * 2], group_number))
        cursor.execute(response_insert_commands,
                       (average_level_command_numbers[(group_number - 1) * 2 + 1], group_number))


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
