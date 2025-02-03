from dataclasses import asdict

from flask import Flask, request
from flask_restful import Api, Resource
from marshmallow.exceptions import ValidationError

from models import (
    init_db,
    get_all_books,
    get_author_list,
    DATA,
    add_book,
    Book
)
from module_17_rest_api.practice.schemas import BookSchema

app: Flask = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self):
        return {'data': [asdict(book) for book in get_all_books()]}, 200

    def post(self):
        data = request.json

        schema = BookSchema()

        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201


api.add_resource(BookList, '/api/books')


class Authors(Resource):
    def get(self):
        return {'data': [asdict(author) for author in get_author_list()]}


api.add_resource(Authors, '/api/authors')
if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
