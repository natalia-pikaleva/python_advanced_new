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
        if len(str(field.data)) < min or len(str(field.data)) > max:
            raise ValidationError

    return _number_length

class NumberLength:
    def __init__(self, min: int, max: int, message: Optional[str] = None):
        self.min = min
        self.max = max

    def __call__(self, form: FlaskForm, field: Field):
        if len(str(field.data)) < self.min or len(str(field.data)) > self.max:
            raise ValidationError

class RegistrationForm(FlaskForm):
    # Использование задекорированной функции
    number1 = IntegerField(validators=[InputRequired(), number_length(min = 10, max = 10)])


    # Использование класса
    number2 = IntegerField(validators=[InputRequired(), NumberLength(min=10, max=10)])




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