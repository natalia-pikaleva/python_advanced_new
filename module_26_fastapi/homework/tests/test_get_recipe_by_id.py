from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

RECIPE_DATA = {"dish_name": "Test1 dish_name",
               "cooking_time": 15,
               "ingredients": "test1_ingredients",
               "description": "test1_description"}


def test_get_recipe_by_id():
    response = client.post("/recipes", json=RECIPE_DATA)
    assert response.status_code == 200

    response = client.get("/recipes/1")
    assert response.status_code == 200


def test_get_recipe_by_non_exist_id():
    response = client.get("/recipes")

    recipes = response.json()
    last_id = len(recipes)
    response = client.get(f"/recipes/{last_id + 1}")

    assert response.status_code == 404

    assert "detail" in response.json()
    assert response.json()["detail"] == "Recipe not found"
