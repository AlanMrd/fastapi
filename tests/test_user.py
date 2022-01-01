from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.json() == {"message": "Hello World Brazil"}
    assert response.status_code == 200

def test_create_users():
    response = client.post("/users/", json={"email":"alanmiranda@gmail.com", "password": "123"})
    print(response.json())