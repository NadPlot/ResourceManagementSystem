from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"documentation": "/docs"}


def test_get_user():
    response = client.get("/v1/user/1")
    assert response.status_code == 200
    assert response.json() == {
        "phone": "+79167003020",
        "login": "rubella19",
        "name": "Анастасия",
        "birth": "2000-07-28",
        "tg": "@Rubella19",
        "email": "anastasia.a.krasnova@gmail.com",
        "id": 1
    }


def test_get_inexistenet_user():
    response = client.get("v1/user/123")
    assert response.status_code == 404
    assert response.json() == {"message": "Пользователь не найден"}
