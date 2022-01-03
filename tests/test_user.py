import pytest
from sqlalchemy.sql import schema
from sqlalchemy.sql.functions import user
from starlette.responses import Response
from app.config import Settings
from app.main import app
from app import schemas
from jose import jwt
from app.config import Settings

settings = Settings()


def test_create_users(client):
    response = client.post("/users", json={"email":"alanmrd@gmail.com", "password": "123"})

    new_user = schemas.User(**response.json())
    assert new_user.email == "alanmrd@gmail.com"
    assert response.status_code == 201

def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(token=login_response.access_token, key=settings.secret_key, algorithms=settings.algorithm)
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

def test_incorret_login(client, test_user):
     response = client.post("/login", data={"username": test_user['email'], "password": "Yeah"})

     response.status_code == 403
     response.json().get("detail") == "The password is wrong"