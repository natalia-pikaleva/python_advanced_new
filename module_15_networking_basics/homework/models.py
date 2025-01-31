import sqlite3
from typing import Any, Optional, List

DATA: dict = {"rooms": [
    {"roomId": 0, "floor": 2, "guestNum": 1, "beds": 1, "price": 2000},
    {"roomId": 1, "floor": 1, "guestNum": 2, "beds": 1, "price": 2500},
    {"roomId": 2, "floor": 1, "guestNum": 2, "beds": 1, "price": 1500}
]}


class Room:

    def __init__(self, id: int, floor: int, guestNum: int, beds: int, price: int, free: bool) -> None:
        self.id = id
        self.floor: int = floor
        self.guestNum: int = guestNum
        self.beds: int = beds
        self.price: int = price
        self.free: bool = free

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)


def init_db(initial_records: List[dict]) -> None:
    with sqlite3.connect('table_rooms.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_rooms'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()
        # now in `exist` we have tuple with table name if table really exists in DB
        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_rooms` (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                floor INTEGER,
                guestNum INTEGER,
                beds INTEGER,
                price INTEGER,
                free BOOL DEFAULT TRUE                
                );
                """

            )

            cursor.executemany(
                """
                INSERT INTO `table_rooms`
                (floor, guestNum, beds, price) VALUES (?, ?, ?, ?)
                """,
                [
                    (item['floor'], item['guestNum'], item['beds'], item['price'])
                    for item in initial_records
                ]
            )
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='table_booking'; 
            """
        )
        exists: Optional[tuple[str,]] = cursor.fetchone()

        if not exists:
            cursor.executescript(
                """
                CREATE TABLE `table_booking` (
                bookingId INTEGER PRIMARY KEY AUTOINCREMENT,
                roomId INTEGER,
                checkIn TEXT,
                checkOut TEXT,
                firstName TEXT,
                lastName TEXT,
                FOREIGN KEY (roomId) REFERENCES table_rooms(id)               
                );
                """
            )

def get_rooms(checkIn: str = "", checkOut: str = "", guestNum: int = 1) -> List[Room]:
    with sqlite3.connect('table_rooms.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * from `table_rooms` tr
                WHERE NOT EXISTS(
                            SELECT 1 FROM table_booking tb 
                            WHERE tr.id = tb.roomId AND checkIn = ? AND checkOut = ?
                    ) AND tr.guestNum >= ?
            """, (checkIn, checkOut, guestNum)
        )

        room_list = [Room(*row) for row in cursor.fetchall()]

        return room_list

def add_room(data: dict) -> None:
    with sqlite3.connect('table_rooms.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()

        response = """
        INSERT INTO table_rooms (floor, guestNum, beds, price) VALUES (?, ?, ?, ?)
        """

        cursor.execute(response, (data['floor'], data['guestNum'], data['beds'], data['price']))
        cursor.connection.commit()

def is_room_free(data):
    with sqlite3.connect('table_rooms.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()


        id = data['roomId']


        cursor.execute(
            """
            SELECT * FROM table_rooms WHERE id = ?
            """, (id, ))
        result = cursor.fetchall()


        if result:
            cursor.execute("""
            SELECT * FROM table_booking WHERE roomId = ? AND checkIn = ? AND checkOut = ?
            """, (data["roomId"], data["bookingDates"]["checkIn"], data["bookingDates"]["checkOut"]))

            booking_record = cursor.fetchall()

            if booking_record:
                return f'На указанные даты номер занят', 409
            else:
                cursor.execute("""
                INSERT INTO table_booking (roomId, checkIn, checkOut, firstName, lastName)
                    VALUES(?, ?, ?, ?, ?)
                """, (data["roomId"], data["bookingDates"]["checkIn"], data["bookingDates"]["checkOut"],
                      data['firstName'], data['lastName']))

                cursor.execute("""
                UPDATE table_rooms SET free = FALSE WHERE id = ?
                """, (data["roomId"], ))
                cursor.connection.commit()

                return f'Номер успешно забронирован', 200

        else:
            return 'Номер с таким id не найден', 400


