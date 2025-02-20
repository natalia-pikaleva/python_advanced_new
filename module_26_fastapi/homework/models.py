from sqlalchemy import Column, String, Integer
from database import Base
# from .database import Base на данный импорт нужно заменить предыдущий
# при запуске тестов, иначе они не работают

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, index=True)
    dish_name = Column(String, index=True)
    count_views = Column(Integer, index=True, default=0)
    cooking_time = Column(Integer, index=True)
    ingredients = Column(String, index=True)
    description = Column(String, index=True)
