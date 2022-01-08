import pydantic
from pydantic.types import Json
import pytest
from app import schemas


def test_get_all_posts(authorized_client, create_posts):
    response = authorized_client.get("/posts")
    assert  response.status_code == 200
    assert response.json()[0]['Post']["title"] == "The most famoust in the joungle"

def test_unauthorized_user_get_all_posts(client):
    response = client.get("/posts")
    response.status_code == 401

def test_get_one_post(authorized_client, create_posts):
    response = authorized_client.get(f"/posts/{create_posts.id}")
    assert response.status_code == 200
    assert  response.json()['Post']['id'] == create_posts.id
    assert  response.json()['Post']['title'] == create_posts.title
    assert  response.json()['Post']['content'] == create_posts.content

def test_get_one_post_does_not_exist(authorized_client):
    response = authorized_client.get("/posts/1000")
    response.status_code == 404
    
@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "I love pepperoni", True),
    ("tallest skycrappers", "wahoo", True)
])    
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts", json={"title": title, "content": content, "published": True})
    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert test_user['id'] == created_post.id

def test_create_post_default_published_true(authorized_client):
    response = authorized_client.post("/posts", json={"title": "new_title", "content": "new_content"})
    created_post = schemas.Post(**response.json())

    assert response.status_code == 201
    assert created_post.published == True

def test_unauthorized_user_create_post(client):
    response = client.post("/posts", json={"title": "new_title", "content": "new_content"})

    assert response.status_code == 401

def test_unauthorized_delete_post(client, create_multiple_posts):
    response = client.delete(f"/posts/{create_multiple_posts[0].id}")
    assert response.status_code == 401

def test_delete_post_not_exist(authorized_client):
    response = authorized_client.delete("/posts/888888")
    assert response.status_code == 404

def test_delete_post(authorized_client, create_multiple_posts):
    response = authorized_client.delete(f"/posts/{create_multiple_posts[0].id}")
    assert response.status_code == 204

def test_delete_other_user_post(authorized_client, create_multiple_posts):
    response = authorized_client.delete(f"/posts/{create_multiple_posts[1].id}")

    assert response.status_code == 403

def test_update_post(authorized_client, create_multiple_posts):
    response = authorized_client.put(f"/posts/{create_multiple_posts[0].id}", 
    json={"title": "title of titles", "content": "contents of content"})

    post_update = schemas.Post(**response.json())
    assert response.status_code == 200
    assert post_update.title == "title of titles"
    assert post_update.content == "contents of content"

def test_update_other_user_post(authorized_client, create_multiple_posts):
    response = authorized_client.put(f"/posts/{create_multiple_posts[1].id}", 
    json={"title": "title of titles", "content": "contents of content"})

    assert response.status_code == 403
    assert response.json().get("detail") == "Not authorized to perform requested action"

def test_update_post_not_exist(authorized_client):
    response = authorized_client.put(f"/posts/99999999", 
    json={"title": "title of titles", "content": "contents of content"})

    assert response.status_code == 404

def test_unauthorized_user_update_post(client, create_multiple_posts):
    response = client.put(f"/posts/{create_multiple_posts[0].id}", json={"title": "new_title", "content": "new_content"})
    assert response.status_code == 401

    