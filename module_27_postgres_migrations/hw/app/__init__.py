from flask import Flask, request, jsonify
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:admin@postgres/skillbox_db'

with app.app_context():
    from .endpoints import get_all_users, insert_user_handler, \
        before_first_request_func, get_coffee_by_name, get_uniq_notes, \
        get_users_by_country


@app.before_first_request
def before_first_request_route():
    return before_first_request_func()


@app.route('/users', methods=['GET'])
def get_users_route():
    return get_all_users()


@app.route('/users', methods=['POST'])
def post_users_route():
    return insert_user_handler()


@app.route('/coffee', methods=['POST'])
def get_coffee_by_name_route():
    return get_coffee_by_name()


@app.route('/uniq_notes', methods=['GET'])
def get_unic_notes_route():
    return get_uniq_notes()

@app.route('/users/country', methods=['POST'])
def get_users_by_country_route():
    return get_users_by_country()
