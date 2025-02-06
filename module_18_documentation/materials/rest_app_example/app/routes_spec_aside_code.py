from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from flask import Flask, request, Response
from flask_restful import Api, Resource
from marshmallow import ValidationError

from models import (
    DATA,
    get_all_books,
    init_db,
    add_book,
)
from schemas import BookSchema

app = Flask(__name__)
api = Api(app)


class BookList(Resource):
    def get(self) -> tuple[list[dict], int]:
        schema = BookSchema()
        return schema.dump(get_all_books(), many=True), 200

    def post(self) -> tuple[dict, int]:
        data = request.data.decode('utf-8')
        schema = BookSchema()
        try:
            book = schema.loads(data)
        except ValidationError as exc:
            return Response(response=str(exc.messages), status=400, mimetype='application/json')

        book = add_book(book)
        return Response(response=schema.dumps(book), status=201, mimetype='application/json')


swagger = Swagger(app, template_file='../swagger.json')
api.add_resource(BookList, '/api/books')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run('0.0.0.0', debug=True)
