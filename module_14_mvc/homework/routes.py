from flask import Flask, render_template
from typing import List

from models import init_db, get_all_books, DATA, get_count_books, add_book_in_db, get_books_of_author, get_book_id
from flask import request

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, Email, NumberRange

app: Flask = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Установите секретный ключ
csrf = CSRFProtect(app)


class RegistrationForm(FlaskForm):
    book_title = StringField(validators=[InputRequired()])
    author_name = StringField(validators=[InputRequired()])


class FindBooksAuthorForm(FlaskForm):
    author_name = StringField(validators=[InputRequired()])


def _get_html_table_for_books(books: List[dict]) -> str:
    table = """
<table>
    <thead>
    <tr>
        <th>ID</td>
        <th>Title</td>
        <th>Author</td>
    </tr>
    </thead>
    <tbody>
        {books_rows}
    </tbody>
</table>
"""
    rows: str = ''
    for book in books:
        rows += '<tr><td>{id}</tb><td>{title}</tb><td>{author}</tb></tr>'.format(
            id=book['id'], title=book['title'], author=book['author'],
        )
    return table.format(books_rows=rows)


@app.route('/books')
def all_books() -> str:
    return render_template(
        'index.html',
        books=get_all_books(), count_books=get_count_books()
    )


@app.route('/books/form', methods=['GET', 'POST'])
def get_books_form() -> str:
    if request.method == 'POST':
        form = RegistrationForm()

        if form.validate_on_submit():
            title, author = form.book_title.data, form.author_name.data
            add_book_in_db(title, author)
            return render_template('successfull_add_book.html')
        else:
            return render_template('nonsuccessfull_add_book.html')

    return render_template('add_book.html')


@app.route('/author', methods=['GET', 'POST'])
def find_books_author() -> str:
    if request.method == 'POST':
        form = FindBooksAuthorForm()

        if form.validate_on_submit():
            author = form.author_name.data
            print(author)
            return render_template(
                'get_books_of_author.html',
                books=get_books_of_author(author),
                author=author,
            )
        else:
            return render_template('nonsuccessfull_author.html')
    return render_template('input_author.html')


@app.route('/books/<int:id>', methods=["GET"])
def books_id(id: int) -> str:
    return render_template(
        'get_book_for_id.html',
        book=get_book_id(id),
        id=id)


if __name__ == '__main__':
    init_db(DATA)
    app.run(debug=True)
