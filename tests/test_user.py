import pytest
from sqlalchemy.sql.functions import user
from starlette.responses import Response
from app.main import app
from app import schemas
from tests.database import session, client

@pytest.fixture()
def test_user(client):
    user_data = {"email":"alanmiranda@gmail.com", "password": "123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data.get('password')
    return new_user


def test_create_users(client):
    response = client.post("/users", json={"email":"alanmrd@gmail.com", "password": "123"})

    new_user = schemas.User(**response.json())
    assert new_user.email == "alanmrd@gmail.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    assert response.status_code == 200
