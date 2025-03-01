from .factories import ClientFactory, ParkingFactory
from module_29_testing.hw.testing_homework.main.models import (
    Client,
    Parking,
)


def test_create_client(app, db):
    client_user = ClientFactory()
    db.session.commit()
    assert client_user.id is not None
    assert len(db.session.query(Client).all()) == 2


def test_create_product(client, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 2
