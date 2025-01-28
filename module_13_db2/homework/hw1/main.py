import sqlite3


def check_if_vaccine_has_spoiled(
        cursor: sqlite3.Cursor,
        truck_number: str
) -> bool:
    response = """
    WITH TruckTable AS (
        SELECT timestamp, temperature_in_celsius 
        FROM table_truck_with_vaccine
        WHERE truck_number = ? 
        ORDER BY timestamp
    )
    SELECT * 
        FROM TruckTable t1
        WHERE EXISTS (
            SELECT 1
            FROM TruckTable t2
            WHERE strftime('%Y-%m-%d %H', t2.timestamp) = strftime('%Y-%m-%d %H', datetime(t1.timestamp, '+1 hour'))
            AND NOT (t1.temperature_in_celsius BETWEEN 18 AND 20)
            AND NOT (t2.temperature_in_celsius BETWEEN 18 AND 20)
        )
        AND EXISTS (
            SELECT 1
            FROM TruckTable t3
            WHERE strftime('%Y-%m-%d %H', t3.timestamp) = strftime('%Y-%m-%d %H', datetime(t1.timestamp, '+2 hour'))
            AND NOT (t1.temperature_in_celsius BETWEEN 18 AND 20)
            AND NOT (t3.temperature_in_celsius BETWEEN 18 AND 20)
        );
    """

    cursor.execute(response, (truck_number,))

    result = cursor.fetchall()
    if not result:
        return False

    return True


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')

    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
