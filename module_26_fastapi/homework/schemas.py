from pydantic import BaseModel


class RecipeForBook(BaseModel):
    dish_name: str
    count_views: int
    cooking_time: int

    class Config:
        from_attributes = True


class RecipeIn(BaseModel):
    dish_name: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeOut(BaseModel):
    dish_name: str
    cooking_time: int
    ingredients: str
    description: str

    class Config:
        orm_mode = True
        from_attributes = True
