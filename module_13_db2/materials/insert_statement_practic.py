import sqlite3

from module_13_db2.materials.insert_statement import input_new_item


class AddingItem:
    def __init__(self, name: str, description: str, amount: int) -> None:
        self.name = name
        self.description = description
        self.amount = amount

    def input_new_item(self) -> "AddingItem":
        name = input('Введите название: ')
        description = input('Введите описание: ')
        amount = int(input('Введите остаток: '))

        return AddingItem(name, description, amount)

if __name__ == "__main__":
    with sqlite3.connect('db_1.db') as conn:
        cursor = conn.cursor()

        new_item = input_new_item()

        cursor.execute("""
        INSERT INTO 'table_warehouse' (name, description, amount) VALUES 
            (?, ?, ?);
        """, (new_item.name, new_item.description, new_item.amount))