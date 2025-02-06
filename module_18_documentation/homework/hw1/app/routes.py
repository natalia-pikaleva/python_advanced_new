from flask import Flask
from flask_restful import Api

from models import DATA, init_db

from resources import BookResource, AuthorResource
from schemas import BookSchema, AuthorSchema
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import APISpec, Swagger
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)
api = Api(app)

spec = APISpec(
    title='BooksList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ],
)

template = spec.to_flasgger(
    app,
    definitions=[BookSchema],
)

swagger = Swagger(app, template=template)

api.add_resource(BookResource, '/api/books', '/api/books/<int:id>')
api.add_resource(AuthorResource, '/api/authors', '/api/authors/<int:id>')

if __name__ == '__main__':
    init_db(initial_records=DATA)
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(debug=True)
