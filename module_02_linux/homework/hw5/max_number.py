"""
Реализуйте endpoint, начинающийся с /max_number, в который можно передать список чисел, разделённых слешем /.
Endpoint должен вернуть текст «Максимальное переданное число {number}»,
где number — выделенное курсивом наибольшее из переданных чисел.

Примеры:

/max_number/10/2/9/1
Максимальное число: 10

/max_number/1/1/1/1/1/1/1/2
Максимальное число: 2

"""

from flask import Flask

app = Flask(__name__)


@app.route("/max_number/<path:numbers_path>")
def max_number(numbers_path: str) -> str:
    '''
    Функция принимает на входе строку из списка чисел, разделенных / и возвращает
    максимальное число, либо надпись, что все элементами должны быть числами
    :param numbers_path: строка из списка чисел, разделенных /
    :return: максимальное число, либо надпись, что все элементами должны быть числами
    '''
    try:
        numbers_list = list(map(float, [num for num in numbers_path.split('/')]))
        max_number = max(numbers_list)
        number = str(max_number)
        return f'Максимальное переданное число <i>{number}</i>'

    except ValueError:
        return "Ошибка: все элементы должны быть числами.", 400


if __name__ == "__main__":
    app.run(debug=True)
