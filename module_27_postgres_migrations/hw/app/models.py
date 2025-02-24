from flask import jsonify
from sqlalchemy import Column, Integer, String, ForeignKey, \
    Boolean, JSON, text, cast, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship
from typing import Dict, Any, Optional
from .database import engine, session
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

Base = declarative_base()


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer(), primary_key=True)
    title = Column(String(200), nullable=False)
    origin = Column(String(200))
    intensifier = Column(String(100))
    notes = Column(JSONB, nullable=True)

    users = relationship("User", back_populates="coffee")


    def __repr__(self):
        return f"Товар {self.title}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False)
    has_sale = Column(Boolean)
    address = Column(JSONB)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))

    coffee = relationship("Coffee", back_populates="users", foreign_keys=[coffee_id])


    def __repr__(self):
        return f"Пользователь {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

def check_tables():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
        tables = [row[0] for row in result]
        logger.info(f"Current tables in the database: {tables}")

def start_bd():
    """
    Создание базы данных при старте
    """
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        logger.info("Tables created successfully.")

        with engine.connect() as connection:
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS idx_coffee_title ON coffee USING gin(to_tsvector('english', title));")
            )
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS idx_user_country ON users USING gin((address->>'country'));")
            )
            logger.info("Indexes created successfully.")

        check_tables()

    except Exception as e:
        logger.error(f"Error during database setup: {e}")


def create_objects(obj):
    """
    Вставка множественных значений в таблицу
    """
    try:
        session.bulk_save_objects(obj)
        session.commit()
    except Exception as e:
        logger.error(f"Error during create object {obj}: {e}")

def get_all(obj):
    """
    Возвращает список всех объектов из таблицы obj
    """
    return session.query(obj).all()


def get_user_by_id(idx: int) -> Optional[User]:
    """Получить пользователя по его ID"""
    user = session.query(User).filter(User.id == idx).one_or_none()

    return user


def create_user(name, address, coffee) -> dict:
    """Создать нового пользователя"""
    logging.debug(f"start create_user with name: {name}, address: {address}, coffee: {coffee}")
    try:
        # Проверьте наличие кофе перед созданием
        if not coffee or not isinstance(coffee.id, int):
            return jsonify({"error": "Invalid coffee provided"}), 400

        logging.debug(f"coffee is success")

        new_user = User(name=name,
                        address=address,
                        coffee=coffee)

        session.add(new_user)
        session.commit()
        logging.debug(f"user added")

        user_id = new_user.id
        logging.debug(f"user_id: {user_id}")

        user = get_user_by_id(user_id)
        logging.debug(f"user: {user}")

        if not user:
            return jsonify({"error": f"User with id {user_id} was not find"}), 400

        user_data = user.to_json()
        user_data["preffered_coffee"] = coffee.to_json()

        return jsonify(user_data), 201

    except Exception as e:
        session.rollback()
        logging.error(e)

        return jsonify({"error": str(e)}), 400


def get_coffee(title):
    """
    Получить информацию о кофе по его названию
    """
    try:
        title = title.lower()

        coffee = session.query(Coffee).filter(
            text("to_tsvector('english', title) @@ plainto_tsquery('english', :title)")
        ).params(title=title).one_or_none()

        if not coffee:
            return jsonify({"error": f"Coffee with title {title} was not find"}), 400

        data_coffee = coffee.to_json()

        return jsonify(data_coffee), 200
    except Exception as e:
        logging.error(f"Error getting coffee: {e}")

        return jsonify({"error": str(e)}), 500


def uniq_notes_coffee():
    """
    Получить список уникальных ноток кофе
    """
    try:
        query = """
                    SELECT DISTINCT unnest(string_to_array(notes::text,', ')) AS note 
                    FROM coffee;
                """

        result = session.execute(text(query)).fetchall()

        if not result:
            return jsonify({"error": f"Notes do not find"}), 400

        notes = [n[0].strip('"') for n in result]

        return jsonify(notes), 200


    except Exception as e:
        logging.error(f"Error getting coffee: {e}")
        return jsonify({"error": str(e)}), 500


def get_users_country(country):
    """
    Получить список пользователей, живущих в конкретной стране
    """
    try:
        country = country.lower()
        users = session.query(User).filter(
            text("address->>'country' ILIKE :country")
        ).params(country=f"%{country}%").all()

        if not users:
            return jsonify({"error": f"Users with country {country} was not find"}), 400

        data_users = [user.to_json for user in users]

        return jsonify(data_users), 200
    except Exception as e:
        logging.error(f"Error getting users with country: {e}")
        return jsonify({"error": str(e)}), 500
