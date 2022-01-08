from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from app.config import Settings
import pytest
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from app.oauth2 import create_acess_token
from app import schemas, models

settings = Settings()

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
             yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture()
def test_user(client):
    user_data = {"email":"alanmiranda@gmail.com", "password": "123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data.get('password')
    return new_user

@pytest.fixture()
def test_user_2(client):
    user_data = {"email":"alan.mrd90@gmail.com", "password": "123"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data.get('password')
    return new_user

@pytest.fixture()
def token(test_user):
    return create_acess_token({"user_id": test_user["id"]})

@pytest.fixture()
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client
    
@pytest.fixture()
def create_posts(authorized_client):
    response = authorized_client.post("/posts", json={"title": "The most famoust in the joungle", "content": "here is"})
    assert response.status_code == 201

    new_post = schemas.Post(**response.json())
    return new_post

@pytest.fixture()
def create_multiple_posts(test_user, test_user_2, session):
    posts_dict = [{"owner_id": test_user['id'], "title": "Title 1", "content": "Content 1"},
    {"owner_id": test_user_2['id'], "title": "Title 2", "content": "Content 2"}]

    def create_post_model(post):
        return models.Post(**post)

    post_map = list(map(create_post_model, posts_dict))

    session.add_all(post_map)
    session.commit()

    posts = session.query(models.Post).all()
    return posts   
    