from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from flasgger import swag_from
from author_spec import author_spec

from models import (
    get_all_books,
    add_book,
    get_book_by_id,
    update_book_by_id,
    delete_book_by_id,
    get_all_authors,
    get_author_by_id,
    get_all_books_of_author,
    add_author,
    delete_author_by_id,
    update_author_by_id
)
from schemas import BookSchema, AuthorSchema


class BookResource(Resource):
    @swag_from('book_api_spec.yaml')
    def get(self, id: int = None) -> tuple[list[dict], int]:

        if id is None:
            schema = BookSchema()
            return schema.dump(get_all_books(), many=True), 200
        else:
            book = get_book_by_id(id)
            if book:
                schema = BookSchema()
                return schema.dump(book), 200
            else:
                return {'message': 'Book not found'}, 404

    @swag_from('book_api_spec.yaml')
    def post(self) -> tuple[dict, int]:

        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        book = add_book(book)
        return schema.dump(book), 201

    @swag_from('book_api_spec.yaml')
    def put(self, id: int) -> tuple[dict, int]:

        data = request.json
        schema = BookSchema()
        try:
            book = schema.load(data)
            updated_book = update_book_by_id(book, id)
            return schema.dump(updated_book), 200
        except ValidationError as exc:
            return exc.messages, 400

    @swag_from('book_api_spec.yaml')
    def delete(self, id: int) -> tuple[dict, int]:

        success = delete_book_by_id(id)
        if success:
            return {'message': f'Book with id {id} has been deleted.'}, 200
        else:
            return {'message': 'Book not found'}, 404

    @swag_from('book_api_spec.yaml')
    def patch(self, id: int) -> tuple[dict, int]:

        data = request.json
        book = get_book_by_id(id)

        if not book:
            return {'message': 'Book not found'}, 404

        if 'title' in data:
            book.title = data['title']

        if 'author' in data:
            author_data = data['author']
            if 'first_name' in author_data:
                book.author.first_name = author_data['first_name']
            if 'last_name' in author_data:
                book.author.last_name = author_data['last_name']
            if 'middle_name' in author_data:
                book.author.middle_name = author_data.get('middle_name', None)

        updated_book = update_book_by_id(book, id)

        schema = BookSchema()
        return schema.dump(updated_book), 200


class AuthorResource(Resource):
    @swag_from(author_spec)
    def get(self, id: int = None) -> tuple[list[dict], int]:

        if id is None:
            schema = AuthorSchema()
            return {"message": schema.dump(get_all_authors(), many=True)}, 200
        else:
            author = get_author_by_id(id)
            if author:
                schema = BookSchema()
                return {"message": schema.dump(get_all_books_of_author(author), many=True)}, 200
            else:
                return {'message': 'Author not found'}, 404

    @swag_from(author_spec)
    def post(self) -> tuple[dict, int]:

        data = request.json
        schema = AuthorSchema()
        try:
            author = schema.load(data)
        except ValidationError as exc:
            return exc.messages, 400

        author = add_author(author)
        return {"message": schema.dump(author)}, 201

    @swag_from(author_spec)
    def delete(self, id: int) -> tuple[dict, int]:

        success = delete_author_by_id(id)
        if success:
            return {'message': f'Author with id {id} has been deleted.'}, 200
        else:
            return {'message': 'Author not found'}, 404

    @swag_from(author_spec)
    def patch(self, id: int) -> tuple[dict, int]:

        data = request.json
        author = get_author_by_id(id)

        if not author:
            return {'message': 'Author not found'}, 404

        if 'author' in data:
            author_data = data['author']
            if 'first_name' in author_data:
                author.first_name = author_data['first_name']
            if 'last_name' in author_data:
                author.last_name = author_data['last_name']
            if 'middle_name' in author_data:
                author.middle_name = author_data.get('middle_name', None)

        updated_author = update_author_by_id(author, id)

        schema = AuthorSchema()
        return {"message": schema.dump(updated_author)}, 200
