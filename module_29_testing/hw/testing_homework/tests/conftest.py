import pytest
from flask import template_rendered
from module_29_testing.hw.testing_homework.main.app import create_app, db as _db
from module_29_testing.hw.testing_homework.main.models import Client, Parking, ClientParking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        client_user = Client(id=1,
                    name="name",
                    surname="surname",
                    credit_card=123456789,
                    car_number='A123AA')
        parking = Parking(id=5,
                          address="address",
                          opened=True,
                          count_places=500,
                          count_available_places=250)
        client_parking = ClientParking(client_id=1,
                                       parking_id=5)

        _db.session.add(client_user)
        _db.session.add(parking)
        _db.session.add(client_parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client

@pytest.fixture
def db(app):
    with app.app_context():
        yield _db