from fastapi.testclient import TestClient
from ..main import app

client = TestClient(app)

RECIPE_DATA1 = {"dish_name": "Test dish_name",
                "cooking_time": 15,
                "description": "test_description"}

RECIPE_DATA2 = {"dish_name": "Test dish_name",
                "cooking_time": "time",
                "ingredients": "test_ingredients",
                "description": "test_description"}

RECIPE_DATA3 = {"dish_name": "Test dish_name",
                "time": 15,
                "ingredients": "test_ingredients",
                "description": "test_description"}


def test_create_recipe_not_field():
    response = client.post("/recipes", json=RECIPE_DATA1)
    assert response.status_code == 422

    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)
    assert len(response.json()["detail"]) == 1

    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", "ingredients"]
    assert error["msg"] == "Field required"


def test_create_recipe_invalid_format():
    response = client.post("/recipes", json=RECIPE_DATA2)
    assert response.status_code == 422

    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)
    assert len(response.json()["detail"]) == 1

    error = response.json()["detail"][0]
    assert error["type"] == "int_parsing"
    assert error["loc"] == ["body", "cooking_time"]
    assert error["msg"] == "Input should be a valid integer, unable to parse string as an integer"


def test_create_recipe_rong_name_field():
    response = client.post("/recipes", json=RECIPE_DATA3)
    assert response.status_code == 422

    assert "detail" in response.json()
    assert isinstance(response.json()["detail"], list)
    assert len(response.json()["detail"]) == 1

    error = response.json()["detail"][0]
    assert error["type"] == "missing"
    assert error["loc"] == ["body", "cooking_time"]
    assert error["msg"] == "Field required"
