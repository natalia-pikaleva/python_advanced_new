"""
Реализуйте приложение для учёта финансов, умеющее запоминать, сколько денег было потрачено за день,
а также показывать затраты за отдельный месяц и за целый год.

В программе должно быть три endpoints:

/add/<date>/<int:number> — сохранение информации о совершённой в рублях трате за какой-то день;
/calculate/<int:year> — получение суммарных трат за указанный год;
/calculate/<int:year>/<int:month> — получение суммарных трат за указанные год и месяц.

Дата для /add/ передаётся в формате YYYYMMDD, где YYYY — год, MM — месяц (от 1 до 12), DD — число (от 01 до 31).
Гарантируется, что переданная дата имеет такой формат и она корректна (никаких 31 февраля).
"""

from flask import Flask

app = Flask(__name__)

storage = {}


@app.route("/add/<date>/<int:number>")
def add(date: str, number: int) -> str:
    '''
    Функция реализует endpoint, принимает на входе дату и сумму расходов
    и записывает данные в словарь
    :param date: дата
    :param number: расходы
    :return: строка о том, что данные успешно добавлены
    '''
    try:
        date_int = int(date)
        if len(date) != 8:
            raise TypeError
    except TypeError:
        return 'Неверный формат даты'
    except ValueError:
        return 'Неверный формат даты'

    year = date[:4]
    month = date[4:6]
    storage.setdefault(year, {}).setdefault(month, 0)
    storage.setdefault(year, {}).setdefault('total', 0)
    storage[year][month] += number
    storage[year]['total'] += number

    return 'Данные успешно добавлены'

@app.route("/calculate/<int:year>")
def calculate_year(year: int) -> str:
    '''
    Функция реализует endpoint, принимает на входе год и возвращает
    расходы за этот год
    :param year: год
    :return: информация о расходах за год year
    '''
    year_str = str(year)  # Преобразуем год в строку
    total = storage.get(year_str, {}).get('total', 0)  # Используем get для безопасного доступа
    return f'Траты за год {year_str} составили: {total}'


@app.route("/calculate/<int:year>/<int:month>")
def calculate_month(year: int, month: int) -> str:
    '''
    Функция реализует endpoint, принимает на входе год и месяц.
    Возвращает расходы за этот месяц
    :param year: год
    :param month: месяц
    :return: информация о расходах за месяц month года year
    '''
    year_str = str(year)  # Преобразуем год в строку
    month_str = str(month).zfill(2)  # Преобразуем месяц в строку и добавляем ноль впереди при необходимости
    total_month = storage.get(year_str, {}).get(month_str, 0)  # Используем get для безопасного доступа
    return f'Траты за месяц {month_str} год {year_str} составили: {total_month}'

if __name__ == "__main__":

    app.run(debug=True)
