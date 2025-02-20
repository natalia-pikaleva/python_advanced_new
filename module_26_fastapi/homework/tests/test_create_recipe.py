from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

RECIPE_DATA = {"dish_name": "Test dish_name",
               "cooking_time": 15,
               "ingredients": "test_ingredients",
               "description": "test_description"}


def test_create_recipe():
    response = client.post("/recipes", json=RECIPE_DATA)
    assert response.status_code == 200
    data = response.json()
    assert data["dish_name"] == RECIPE_DATA["dish_name"]
    assert data["cooking_time"] == RECIPE_DATA["cooking_time"]
    assert data["ingredients"] == RECIPE_DATA["ingredients"]
    assert data["description"] == RECIPE_DATA["description"]
