import json
import pytest
from module_29_testing.hw.testing_homework.main.app import db as _db
from module_29_testing.hw.testing_homework.main.models import (
    Client,
    Parking,
    ClientParking,
)


def test_math_route(client) -> None:
    resp = client.get("/test_route?number=8")
    data = json.loads(resp.data.decode())
    assert data == 64


def test_client(client) -> None:
    resp = client.get("/clients/1")
    assert resp.status_code == 200
    assert resp.json == {
        "id": 1,
        "name": "name",
        "surname": "surname",
        "credit_card": "123456789",
        "car_number": "A123AA",
    }


def test_create_client(client) -> None:
    client_data = {
        "name": "Никита",
        "surname": "Нестеренко",
        "credit_card": 987654321,
        "car_number": "T000TT",
    }
    resp = client.post("/clients", data=client_data)

    assert resp.status_code == 201


def test_create_parking(client) -> None:
    parking_data = {
        "address": "address",
        "opened": True,
        "count_places": 1000,
        "count_available_places": 800,
    }
    resp = client.post("/parking", data=parking_data)

    assert resp.status_code == 201


def test_go_to_parking(client) -> None:
    for i in range(3):
        client_user_data = {
            "name": f"Никита {i}",
            "surname": f"Нестеренко {i}",
            "credit_card": 987654321 + i,
            "car_number": f"T{i}000TT",
        }
        resp = client.post("/clients", data=client_user_data)
        assert resp.status_code == 201

    parking_data = {
        "address": "address",
        "opened": "True",
        "count_places": 1000,
        "count_available_places": 800,
    }
    resp = client.post("/parking", data=parking_data)
    assert resp.status_code == 201

    parking_id = _db.session.query(Parking).first().id

    client_users = _db.session.query(Client).all()
    for client_user in client_users:
        client_parking = (
            _db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_user.id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
            )
            .one_or_none()
        )
        if client_parking is None:
            client_user_id = client_user.id
            break

    parking = _db.session.query(Parking).get(parking_id)
    assert parking.opened == True
    assert parking.count_available_places > 0

    client_parking_data = {"client_id": client_user_id, "parking_id": parking_id}

    resp = client.post("/client_parking", data=client_parking_data)

    assert resp.status_code == 201


def test_go_to_closed_parking(client) -> None:
    client_user_data = {
        "name": f"Петр",
        "surname": f"Иванов",
        "credit_card": 987654321,
        "car_number": f"T000TT",
    }
    resp = client.post("/clients", data=client_user_data)
    assert resp.status_code == 201

    parking_data = {
        "address": "address_closed_parking",
        "opened": False,
        "count_places": 1000,
        "count_available_places": 800,
    }
    resp = client.post("/parking", data=parking_data)
    assert resp.status_code == 201

    parking_id, *_ = (
        _db.session.query(Parking.id)
        .filter(Parking.address == "address_closed_parking")
        .first()
    )

    client_users = _db.session.query(Client).all()
    for client_user in client_users:
        client_parking = (
            _db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_user.id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
            )
            .one_or_none()
        )
        if client_parking is None:
            client_user_id = client_user.id
            break

    parking = _db.session.query(Parking).get(parking_id)
    assert parking.opened == False

    client_parking_data = {"client_id": client_user_id, "parking_id": parking_id}

    resp = client.post("/client_parking", data=client_parking_data)

    assert resp.status_code == 404
    assert resp.json["message"] == "Извините, парковка закрыта"


def test_not_places_on_the_parking(client) -> None:
    client_user_data = {
        "name": f"Петр",
        "surname": f"Иванов",
        "credit_card": 987654321,
        "car_number": f"T000TT",
    }
    resp = client.post("/clients", data=client_user_data)
    assert resp.status_code == 201

    parking_data = {
        "address": "address_parking_without_places",
        "opened": True,
        "count_places": 800,
        "count_available_places": 0,
    }
    resp = client.post("/parking", data=parking_data)
    assert resp.status_code == 201

    parking_id, *_ = (
        _db.session.query(Parking.id)
        .filter(Parking.address == "address_parking_without_places")
        .first()
    )

    client_users = _db.session.query(Client).all()
    for client_user in client_users:
        client_parking = (
            _db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_user.id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
            )
            .one_or_none()
        )
        if client_parking is None:
            client_user_id = client_user.id
            break

    parking = _db.session.query(Parking).get(parking_id)
    assert parking.count_available_places == 0

    client_parking_data = {"client_id": client_user_id, "parking_id": parking_id}

    resp = client.post("/client_parking", data=client_parking_data)

    assert resp.status_code == 404
    assert resp.json["message"] == "Извините, на парковке нет cвободных мест"


def test_client_entered_to_parking_earlier(client):
    client_user_data = {
        "name": f"Петр",
        "surname": f"Иванов",
        "credit_card": 987654321,
        "car_number": f"T000TT",
    }
    resp = client.post("/clients", data=client_user_data)
    assert resp.status_code == 201

    parking_data = {
        "address": "address_parking_for_go_to_twice",
        "opened": True,
        "count_places": 800,
        "count_available_places": 800,
    }
    resp = client.post("/parking", data=parking_data)
    assert resp.status_code == 201

    parking_id, *_ = (
        _db.session.query(Parking.id)
        .filter(Parking.address == "address_parking_for_go_to_twice")
        .first()
    )

    client_users = _db.session.query(Client).all()
    for client_user in client_users:
        client_parking = (
            _db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_user.id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
            )
            .one_or_none()
        )
        if client_parking is None:
            client_user_id = client_user.id
            break

    client_parking_data = {"client_id": client_user_id, "parking_id": parking_id}

    # Добавляем клиента на парковку первый раз
    resp = client.post("/client_parking", data=client_parking_data)
    assert resp.status_code == 201

    # Добавляем клиента на парковку второй раз
    resp = client.post("/client_parking", data=client_parking_data)
    assert resp.status_code == 404
    assert (
        resp.json["message"]
        == f"Клиент с id {client_user_id} уже въехал на парковку c id {parking_id}"
    )


def test_go_out_parking(client):
    client_user_data = {
        "name": f"Петр",
        "surname": f"Иванов",
        "credit_card": 987654321,
        "car_number": f"T000TT",
    }
    resp = client.post("/clients", data=client_user_data)
    assert resp.status_code == 201

    parking_data = {
        "address": "address_parking_for_check_go_out",
        "opened": True,
        "count_places": 800,
        "count_available_places": 800,
    }
    resp = client.post("/parking", data=parking_data)
    assert resp.status_code == 201

    parking_id, *_ = (
        _db.session.query(Parking.id)
        .filter(Parking.address == "address_parking_for_check_go_out")
        .first()
    )

    client_users = _db.session.query(Client).all()
    for client_user in client_users:
        client_parking = (
            _db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_user.id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
            )
            .one_or_none()
        )
        if client_parking is None:
            client_user_id = client_user.id
            break

    client_parking_data = {"client_id": client_user_id, "parking_id": parking_id}

    # Добавляем клиента на парковку
    resp = client.post("/client_parking", data=client_parking_data)
    assert resp.status_code == 201

    # Клиент уезжает с парковки
    resp = client.delete("/client_parking", data=client_parking_data)
    assert resp.status_code == 201


def test_app_config(app):
    assert not app.config["DEBUG"]
    assert app.config["TESTING"]
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite://"


@pytest.mark.parametrize("route", ["/test_route?number=8", "/clients/1", "/clients"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200
