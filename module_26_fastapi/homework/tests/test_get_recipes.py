from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

RECIPE_DATA_LIST = [
    {"dish_name": "Test1 dish_name",
     "cooking_time": 15,
     "ingredients": "test1_ingredients",
     "description": "test1_description"},

    {"dish_name": "Test2 dish_name",
     "cooking_time": 20,
     "ingredients": "test2_ingredients",
     "description": "test2_description"},

    {"dish_name": "Test2 dish_name",
     "cooking_time": 25,
     "ingredients": "test2_ingredients",
     "description": "test2_description"}
]


def test_get_recipes():
    for data in RECIPE_DATA_LIST:
        response = client.post("/recipes", json=data)

    response = client.get("/recipes")
    assert response.status_code == 200

    recipes = response.json()

    for recipe_data in RECIPE_DATA_LIST:
        assert any(
            recipe["dish_name"] == recipe_data["dish_name"] and
            recipe["cooking_time"] == recipe_data["cooking_time"]
            for recipe in recipes
        ), f"Recipe {recipe_data['dish_name']} not found in the response"


def test_get_sorted_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200

    recipes = response.json()

    sorted_recipes = sorted(recipes, key=lambda x: (-x["count_views"], x["cooking_time"]))

    assert recipes == sorted_recipes
