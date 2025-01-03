"""
Довольно неудобно использовать встроенный валидатор NumberRange для ограничения числа по его длине.
Создадим свой для поля phone. Создайте валидатор обоими способами.
Валидатор должен принимать на вход параметры min и max — минимальная и максимальная длина,
а также опциональный параметр message (см. рекомендации к предыдущему заданию).
"""
from typing import Optional

from flask_wtf import FlaskForm
from wtforms import Field

from flask import Flask
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, ValidationError

app = Flask(__name__)

def number_length(min: int, max: int, message: Optional[str] = None):

    def _number_length(form: FlaskForm, field: Field):
        if field.data < min or field.data > max:
            # TODO В задании имелась ввиду проверка разрядности (в тексте задания "длины") числа, это значительно удобнее,
            #  чем указывать само число, особенно если оно очень большое
            raise ValidationError

    return _number_length

class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max

    def __call__(self, form: FlaskForm, field: Field):
        if field.data < self.min or field.data > self.max:
            # TODO Аналогично предыдущему
            raise ValidationError

class RegistrationForm(FlaskForm):
    # Использование задекорированной функции
    number1 = IntegerField(validators=[InputRequired(), number_length(min = 1000000000, max = 9999999999)])
    # TODO правильно указать min=10, max=10

    # Использование класса
    number2 = IntegerField(validators=[InputRequired(), NumberLength(min=1000000000, max=9999999999)])




@app.route("/registration", methods=["POST"])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        number1, number2 = form.number1.data, form.number2.data

        return f"Successfully registered user with phone +7{number1} and second phone +7{number2}"

    return f"Invalid input, {form.errors}", 400

if __name__ == "__main__":
    app.config["WTF_CSRF_ENABLED"] = False
    app.run(debug=True)