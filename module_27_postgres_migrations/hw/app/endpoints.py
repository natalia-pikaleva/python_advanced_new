from flask import request, jsonify
from .models import Coffee, User, start_bd, create_objects, \
    get_all, create_user, get_coffee, uniq_notes_coffee, get_users_country
import requests
import random
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

NAMES = ["Viktor", "Ivan", "Petr", "Natalya", "Ekaterina", "Anna", "Olga", "Ksenija", "Maria", "Anton"]
ADDRESS_LIST = [{"id":5099,"uid":"d32d5917-5e38-48f8-a029-052ef766f33f","city":"South Catherinafurt","street_name":"Ewa Mission","street_address":"648 Fay Turnpike","secondary_address":"Suite 297","building_number":"3370","mail_box":"PO Box 68","community":"Eagle Acres","zip_code":"72471-4234","zip":"57646-3386","postcode":"03267","time_zone":"Pacific/Pago_Pago","street_suffix":"Pine","city_suffix":"port","city_prefix":"Lake","state":"Kansas","state_abbr":"RI","country":"Qatar","country_code":"VC","latitude":-61.62785550302492,"longitude":75.4799219661873,"full_address":"134 Harber Hollow, Lake Lakiesha, TN 97172-4929"},
                {"id":5717,"uid":"f78b29a8-8f0f-4579-92f7-e5872a785c29","city":"Tannerbury","street_name":"Hartmann Via","street_address":"28673 Luigi Turnpike","secondary_address":"Apt. 932","building_number":"608","mail_box":"PO Box 657","community":"Pine Creek","zip_code":"58653","zip":"00566","postcode":"58660-0986","time_zone":"America/Bogota","street_suffix":"Roads","city_suffix":"ville","city_prefix":"East","state":"California","state_abbr":"MT","country":"Saint Helena","country_code":"AI","latitude":-73.48470516318848,"longitude":27.430708054313897,"full_address":"Apt. 130 5530 Alberto Burgs, Christiansenbury, FL 91588-2382"},
                {"id":5191,"uid":"8be723a7-e289-4fc2-9432-928047daab31","city":"Port Mozellaberg","street_name":"Hammes Mountains","street_address":"2208 Howe Valleys","secondary_address":"Suite 265","building_number":"134","mail_box":"PO Box 4322","community":"Pine Place","zip_code":"11648","zip":"82383","postcode":"98318","time_zone":"Asia/Tokyo","street_suffix":"Mountain","city_suffix":"ville","city_prefix":"East","state":"South Carolina","state_abbr":"MO","country":"Denmark","country_code":"CY","latitude":0.6800014610538625,"longitude":53.62558131903589,"full_address":"747 Kris Falls, Port Alex, MN 76080-6816"},
                {"id":7177,"uid":"92bbacdf-e8ac-4fb5-8919-091ea8aa0088","city":"East Gilton","street_name":"Thompson Avenue","street_address":"59298 Mohamed Parks","secondary_address":"Apt. 238","building_number":"657","mail_box":"PO Box 24","community":"Park Village","zip_code":"47874-4293","zip":"33738","postcode":"17045-1659","time_zone":"Europe/Minsk","street_suffix":"Prairie","city_suffix":"burgh","city_prefix":"Port","state":"North Carolina","state_abbr":"MO","country":"Sweden","country_code":"NU","latitude":25.118960078891448,"longitude":-172.78587847384182,"full_address":"613 Hand Radial, Buckridgeland, WI 77885"},
                {"id":8051,"uid":"79c0ea1d-f8da-402e-b088-c29a4e56a078","city":"Kingbury","street_name":"Corwin Points","street_address":"854 Renner Spring","secondary_address":"Suite 903","building_number":"13437","mail_box":"PO Box 57","community":"Park Estates","zip_code":"10438-1080","zip":"78464-8759","postcode":"65948","time_zone":"Pacific/Pago_Pago","street_suffix":"Rue","city_suffix":"burgh","city_prefix":"New","state":"Maryland","state_abbr":"WY","country":"Burkina Faso","country_code":"GB","latitude":-24.444316717453404,"longitude":58.06164178752468,"full_address":"22928 Nita Spurs, Fredericport, DE 92273-9179"},
                {"id":6982,"uid":"a4f48e7f-d0ab-4da2-ba2e-39eb34c934d6","city":"South Jamie","street_name":"Sanford Roads","street_address":"9412 Garth Forge","secondary_address":"Apt. 605","building_number":"460","mail_box":"PO Box 5864","community":"Willow Court","zip_code":"60036","zip":"28951","postcode":"33605","time_zone":"Asia/Bangkok","street_suffix":"Brook","city_suffix":"ville","city_prefix":"Lake","state":"Nevada","state_abbr":"SD","country":"Bolivia","country_code":"NG","latitude":0.3434203509896463,"longitude":33.58295376055642,"full_address":"Apt. 765 407 Heathcote Dale, South Francisfort, SD 53473-3001"},
                {"id":2004,"uid":"ad9a6c77-1824-44f9-a928-bf43f7b65184","city":"South Jessie","street_name":"Ryann View","street_address":"768 Cronin Square","secondary_address":"Apt. 919","building_number":"554","mail_box":"PO Box 623","community":"University Crossing","zip_code":"74849","zip":"70622-3393","postcode":"39422-4782","time_zone":"America/Tijuana","street_suffix":"Ranch","city_suffix":"stad","city_prefix":"Lake","state":"New York","state_abbr":"NY","country":"Finland","country_code":"LA","latitude":-1.672282163841274,"longitude":-39.155002871957635,"full_address":"Apt. 714 503 Streich Pine, Lake Reyna, OH 62509"},
                {"id":2529,"uid":"0c131b7c-607e-4c58-bfa5-81815a013083","city":"New Rosalia","street_name":"Halvorson Groves","street_address":"43521 Donny Mews","secondary_address":"Suite 236","building_number":"678","mail_box":"PO Box 472","community":"University Square","zip_code":"76736-5750","zip":"02996-9433","postcode":"84962","time_zone":"Europe/Lisbon","street_suffix":"Canyon","city_suffix":"port","city_prefix":"Port","state":"Indiana","state_abbr":"OH","country":"Romania","country_code":"BQ","latitude":-32.71674784961973,"longitude":-12.71826489760312,"full_address":"Apt. 962 88685 Dean Gateway, New Janaeview, AR 82495"},
                {"id":5713,"uid":"3be1c9b4-d94f-450d-aaac-6296ca9ad9c7","city":"Port Sierra","street_name":"Farrell Crossroad","street_address":"934 Goodwin Mountains","secondary_address":"Apt. 303","building_number":"870","mail_box":"PO Box 28","community":"Willow Estates","zip_code":"34591-8935","zip":"93528-2768","postcode":"51854-6836","time_zone":"Europe/Skopje","street_suffix":"Fords","city_suffix":"shire","city_prefix":"West","state":"Alabama","state_abbr":"OK","country":"Honduras","country_code":"PT","latitude":-70.18590446276468,"longitude":44.93236978765324,"full_address":"654 Florentino Pass, Mohrborough, MS 74657-3308"},
                {"id":5066,"uid":"995ef27f-46e8-4420-a4f8-43c5d3c170a6","city":"Micheleport","street_name":"Jennifer Pine","street_address":"1582 Flo Turnpike","secondary_address":"Apt. 193","building_number":"682","mail_box":"PO Box 604","community":"University Heights","zip_code":"78018","zip":"95751-5134","postcode":"56660","time_zone":"Asia/Singapore","street_suffix":"Green","city_suffix":"shire","city_prefix":"New","state":"Hawaii","state_abbr":"OR","country":"Guatemala","country_code":"SD","latitude":69.85521503141143,"longitude":-32.420154255987995,"full_address":"Apt. 562 393 McKenzie Meadow, Raleighborough, KY 82051-6700"}]

def get_random_coffee():
    """
    Делает GET-запрос к API и возвращает данные о случайном кофе
    """
    url = "https://random-data-api.com/api/coffee/random_coffee"
    try:
        response = requests.get(url)

        response.raise_for_status()

        data_coffee = response.json()
        logging.debug(f"notes: {data_coffee}")

        return data_coffee

    except requests.exceptions.RequestException:
        return None


def get_random_address(idx):
    """
    Делает GET-запрос к API и возвращает случайный адрес
    """
    url = "https://random-data-api.com/api/address/random_address"
    try:
        # response = requests.get(url)
        # response.raise_for_status()
        # data = response.json()

        data = ADDRESS_LIST[idx]
        # Извлекаем нужные поля
        street_address = data.get('street_address')
        city = data.get('city')
        state = data.get('state')
        country = data.get('country')

        # Формируем строку адреса
        full_address = {"street_address": street_address, "city": city, "state": state, "country": country}

        return full_address

    except requests.exceptions.RequestException:
        return None


def before_first_request_func():
    """
    При первом запуске создает базу данных и заполнят таблицы с кофе и пользователями
    """
    try:
        start_bd()

        coffee_list = []
        users_list = []

        # Создаем 10 кофе
        for id in range(10):
            data_coffee = get_random_coffee()
            if data_coffee:
                coffee = Coffee(
                    id=data_coffee["id"],
                    title=data_coffee["blend_name"],
                    origin=data_coffee["origin"],
                    intensifier=data_coffee["intensifier"],
                    notes=data_coffee["notes"]
                )
                coffee_list.append(coffee)

        # Сохраняем кофе в базу данных
        create_objects(coffee_list)

        # Получаем все сохраненные кофе для рандомного выбора
        saved_coffees = get_all(Coffee)

        # Создаем 10 пользователей и присваиваем им случайное кофе
        for idx in range(10):
            user = User(
                name=NAMES[idx],
                address=get_random_address(idx),
                coffee_id=random.choice(saved_coffees).id  # Присваиваем случайное кофе
            )
            users_list.append(user)

        # Сохраняем пользователей в базу данных
        create_objects(users_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def insert_user_handler():
    """
    Вставляет нового пользователя в базу данных
    """
    try:
        if not request.is_json:
            logging.error("Missing JSON in request")
            return jsonify({"error": "Missing JSON in request"}), 400

        data = request.get_json()
        if not data or "name" not in data or "address" not in data:
            return jsonify({"error": "Missing required parameters: name or address"}), 400

        name = data["name"]
        address = data["address"]

        if ("city" not in address) or ("street_address" not in address) or ("state" not in address):
            return jsonify({"error": "Invalid address format"}), 400

        saved_coffees = get_all(Coffee)
        if not saved_coffees:
            return jsonify({"error": "No coffees available"}), 400

        coffee = random.choice(saved_coffees)
        if not coffee:
            return jsonify({"error": "Could not retrieve coffee"}), 400

        logging.debug(f"coffee for new user: {coffee}")
        logging.debug(f"notes: {coffee.notes}")

        user_data = create_user(name=name, address=address, coffee=coffee)

        return user_data

    except Exception as e:
        logging.error(f"Error getting coffee: {e}")
        return jsonify({"error": str(e)}), 400


def get_all_users():
    """
    Возвращает информацию о всех пользователях
    """
    try:
        users = get_all(User)

        user_list = [user.to_json() for user in users]

        return jsonify(user_list), 200
    except Exception as e:
        logging.error(f"Error getting coffee: {e}")
        return jsonify({"error": str(e)}), 400


def get_coffee_by_name():
    """
    Возвращает информацию о кофе по его имени
    """
    try:
        if not request.is_json:
            logging.error("Missing JSON in request")
            return jsonify({"error": "Missing JSON in request"}), 400

        data = request.get_json()
        if not data or "title" not in data:
            return jsonify({"error": "Missing required parameters: title"}), 400

        title = data["title"]

        result = get_coffee(title)

        return result


    except Exception as e:
        logging.error(f"Error getting coffee: {e}")
        return jsonify({"error": str(e)}), 400


def get_uniq_notes():
    """
    Возвращает список уникальных ноток
    """
    try:
        result = uniq_notes_coffee()
        return result


    except Exception as e:
        logging.error(f"Error getting coffee: {e}")
        return jsonify({"error": str(e)}), 400


def get_users_by_country():
    """
    Возвращает список пользователей, проживающих в определенной стране
    """
    try:
        if not request.is_json:
            logging.error("Missing JSON in request")
            return jsonify({"error": "Missing JSON in request"}), 400

        data = request.get_json()
        if not data or "country" not in data:
            return jsonify({"error": "Missing required parameters: country"}), 400

        country = data["country"]

        result = get_users_country(country)

        return result


    except Exception as e:
        logging.error(f"Error getting coffee: {e}")
        return jsonify({"error": str(e)}), 400
