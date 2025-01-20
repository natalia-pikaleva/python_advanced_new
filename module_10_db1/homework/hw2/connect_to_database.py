import sqlite3

if __name__ == "__main__":
    with sqlite3.connect("hw_2_database.db") as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT p.colour, COUNT(*) as purchaise_count "
                       "FROM 'table_checkout' c JOIN `table_phones` p ON c.phone_id = p.id "
                       "GROUP BY p.colour "
                       "ORDER BY purchaise_count DESC ")

        result = cursor.fetchall()

        colour_dict = dict(result)

        with open('report.md', 'w') as file:
            file.write('#Отчет о покупках телефонов:\n\n')
            file.write('##1.Телефоны какого цвета покупают чаще всего:\n\n')
            colour, count = list(colour_dict.items())[0]
            file.write(f'Цвет телефона: **{colour}**\n\n')
            file.write(f'Количество покупок: **{count}**\n\n')

            file.write('##2. Какие телефоны покупают чаще: синие или красные:\n\n')
            file.write(f'Количество красных телефонов: **{colour_dict['красный']}**\n\n')
            file.write(f'Количество синих телефонов: **{colour_dict['синий']}**\n\n')
            if colour_dict['красный'] > colour_dict['синий']:
                file.write(f'Красные телефоны покупают чаще\n\n')
            elif colour_dict['красный'] < colour_dict['синий']:
                file.write(f'Синие телефоны покупают чаще\n\n')
            else:
                file.write(f'Количество покупок красных и синих телефонов одинаково\n')

            colour, count = list(colour_dict.items())[-1]
            file.write('##3. Какой самый непопулярный цвет телефонов:\n\n')
            file.write(f'Цвет телефона: **{colour}**\n\n')
            file.write(f'Количество покупок: **{count}**\n\n')