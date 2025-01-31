import pprint
import json
from flask import Flask, jsonify, request
from models import init_db, DATA, get_rooms, add_room, is_room_free

app: Flask = Flask(__name__)

@app.route('/room', methods=['GET'])
def get_room():
    try:
        checkIn = request.args.get("checkIn")
        checkOut = request.args.get("checkOut")
        guestNum = int(request.args.get("guestNum"))

        room_list = get_rooms(checkIn, checkOut, guestNum)
        room_data = [{'roomId': room['id'], 'floor': room['floor'], 'guestNum': room['guestNum'], 'beds': room['beds'],
                      'price': room['price'], 'free': room['free']} for room in room_list]


        return jsonify({'rooms': room_data}), 200
    except Exception as ex:
        return jsonify(error=str(ex)), 500

@app.route('/add-room', methods=['POST'])
def add_room_in_bd():
    try:
        data = request.json

        if data:
            add_room(data)
            return f'Номер успешно добавлен', 200

        else:
            return f'Нет данных', 500
    except Exception as ex:
        return jsonify(error=str(ex)), 500

@app.route('/booking', methods=['POST'])
def booking():
    try:
        data = request.json

        if data:
            return is_room_free(data)

        else:
            return f'Нет данных', 500
    except Exception as ex:
        return jsonify(error=str(ex)), 500

if __name__ == '__main__':
    init_db(DATA["rooms"])

    app.run(debug=True)