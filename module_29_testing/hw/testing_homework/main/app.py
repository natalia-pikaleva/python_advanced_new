from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List
import datetime

db = SQLAlchemy()

db_created = False


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, Parking, ClientParking

    @app.before_request
    def before_request_func():
        global db_created
        if not db_created:
            db.create_all()
            db_created = True

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/test_route")
    def math_route():
        """Тестовый роут для расчета степени"""
        number = int(request.args.get("number", 0))
        result = number**2
        return jsonify(result)

    @app.route("/clients", methods=["POST"])
    def create_client_handler():
        """Создание нового клиента"""
        name = request.form.get("name", type=str)
        surname = request.form.get("surname", type=str)
        credit_card = request.form.get("credit_card", type=int)
        car_number = request.form.get("car_number", type=str)

        new_client = Client(
            name=name, surname=surname, credit_card=credit_card, car_number=car_number
        )

        try:
            db.session.add(new_client)
            db.session.commit()

            return "", 201
        except Exception as e:
            db.session.rollback()
            return f"Ошибка при обновлении данных: {e}", 500

    @app.route("/clients", methods=["GET"])
    def get_clients_handler():
        """Получение клиентов"""
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [u.to_json() for u in clients]
        return jsonify(clients_list), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_handler(client_id: int):
        """Получение клиента по ид"""
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route("/parking", methods=["POST"])
    def create_parking_handler():
        """Создание нового паркинга"""
        address = request.form.get("address", type=str)
        opened = request.form.get("opened", type=str)
        if opened.lower() == "true":
            opened = True
        else:
            opened = False
        count_places = request.form.get("count_places", type=int)
        count_available_places = request.form.get("count_available_places", type=int)

        if count_places <= 0:
            return jsonify({"message":
                f"Ошибка при создании парковки, количество мест на парковке "
                f"должно быть больше 0"}), 404

        if count_available_places < 0 or count_available_places > count_places:
            return jsonify({"message":
                f"Ошибка при создании парковки, количество свободных мст должно быть "
                f"в диапазоне от 0 до количества всех мест"}
            ), 404

        new_parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places,
        )

        try:
            db.session.add(new_parking)
            db.session.commit()
            return "", 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Ошибка при обновлении данных: {e}"}), 500

    @app.route("/client_parking", methods=["POST"])
    def go_to_parking_handler():
        """Заезд клиента на парковку"""
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)

        client: Client = db.session.query(Client).get(client_id)
        parking: Parking = db.session.query(Parking).get(parking_id)

        if not client:
            return jsonify({"message": f"Клиент с id {client_id} не найден"}), 404

        if not parking:
            return jsonify({"message": "Парковка с id {parking_id} не найдена"}), 404

        if not parking.opened:
            return jsonify({"message": "Извините, парковка закрыта"}), 404

        if parking.count_available_places == 0:
            return jsonify({"message": "Извините, на парковке нет cвободных мест"}), 404

        client_parking: ClientParking = (
            db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
            )
            .one_or_none()
        )

        if client_parking:
            return (
                jsonify({"message": f"Клиент с id {client_id} уже въехал на парковку c id {parking_id}"}),
                404,
            )

        new_client_parking = ClientParking(
            client_id=client_id, parking_id=parking_id, time_in=datetime.datetime.now()
        )

        parking.count_available_places -= 1

        try:
            db.session.add(new_client_parking)
            db.session.commit()
            return "", 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Ошибка при обновлении данных: {e}"}), 500

    @app.route("/client_parking", methods=["DELETE"])
    def go_out_parking_handler():
        """Выезд клиента с парковки"""
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)

        client: Client = db.session.query(Client).get(client_id)
        parking: Parking = db.session.query(Parking).get(parking_id)

        if not client:
            return jsonify({"message": f"Клиент с id {client_id} не найден"}), 404

        if not parking:
            return jsonify({"message": f"Парковка с id {parking_id} не найдена"}), 404

        client_parking: ClientParking = (
            db.session.query(ClientParking)
            .filter(
                ClientParking.client_id == client_id,
                ClientParking.parking_id == parking_id,
                ClientParking.time_out.is_(None),
            )
            .one_or_none()
        )

        if not client_parking:
            return jsonify({"message":
                f"Клиент с id {client_id} не въезжал на парковку c id {parking_id}"}), 404



        if not client.credit_card:
            return jsonify({"message": f"При оплате произошла ошибка"}), 404

        client_parking.time_out = datetime.datetime.now()
        parking.count_available_places += 1

        try:
            db.session.commit()
            return "", 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Ошибка при обновлении данных: {e}"}), 500

    return app
