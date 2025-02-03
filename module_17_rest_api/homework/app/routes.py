from flask import Flask
from flask_restful import Api

from models import DATA, init_db

from resources import BookResource, AuthorResource

app = Flask(__name__)
api = Api(app)

api.add_resource(BookResource, '/api/books', '/api/books/<int:id>')
api.add_resource(AuthorResource, '/api/authors', '/api/authors/<int:id>')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    app.run(debug=True)
