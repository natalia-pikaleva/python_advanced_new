import factory
from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker, SubFactory, LazyAttribute
from factory.fuzzy import FuzzyInteger
import random
import datetime

from module_29_testing.hw.testing_homework.main.app import db
from module_29_testing.hw.testing_homework.main.models import (
    Client,
    Parking,
    ClientParking,
)

import string


def generate_car_number():
    # Список русских букв, используемых в номерах
    letters = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЭЮЯ"

    # Генерация случайных букв и цифр
    first_letters = "".join(random.choice(letters) for _ in range(3))
    numbers = "".join(random.choice(string.digits) for _ in range(3))
    last_letters = "".join(random.choice(letters) for _ in range(2))

    # Формирование номера
    car_number = f"{first_letters}{numbers}{last_letters}"

    return car_number


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = Faker("first_name")
    surname = Faker("last_name")
    credit_card = Faker("credit_card_number")
    car_number = LazyAttribute(lambda x: generate_car_number())


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = Faker("address")
    opened = LazyAttribute(lambda x: random.choice([True, False]))
    count_places = FuzzyInteger(100, 1000)

    @factory.lazy_attribute
    def count_available_places(self):
        return random.randrange(0, self.count_places + 1)


class ClientParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = ClientParking
        sqlalchemy_session = db.session

    client = SubFactory(ClientFactory)
    parking = SubFactory(ParkingFactory)
    time_in = LazyAttribute(
        lambda x: datetime.datetime.now()
        - datetime.timedelta(hours=random.randint(1, 24))
    )
    time_out = LazyAttribute(
        lambda x: x.time_in + datetime.timedelta(hours=random.randint(1, 24))
    )
