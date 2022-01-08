import pytest
from app import models

@pytest.fixture()
def post_voted(session, create_multiple_posts, test_user):
    new_vote = models.Vote(post_id=create_multiple_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)

def test_create_vote(authorized_client, create_multiple_posts):
    response = authorized_client.post("/vote", json={"post_id": create_multiple_posts[0].id, "dir": 1})

    assert response.status_code == 201

def test_twice_vote(authorized_client, create_multiple_posts, post_voted):
    response = authorized_client.post("/vote", json={"post_id": create_multiple_posts[0].id, "dir": 1})

    assert response.status_code == 409

def test_delete_vote(authorized_client, create_multiple_posts, post_voted):
    response = authorized_client.post("/vote", json={"post_id": create_multiple_posts[0].id, "dir": 0})

    assert response.status_code == 201

def test_delete_vote_non_exist(authorized_client, create_multiple_posts):
    response = authorized_client.post("/vote", json={"post_id": create_multiple_posts[1].id, "dir": 0})

    assert response.status_code == 404

def test_vote_post_non_exist(authorized_client, create_multiple_posts):
    response = authorized_client.post("/vote", json={"post_id": 8, "dir": 1})

    assert response.status_code == 404

def test_vote_user_unauthorized(client, create_multiple_posts):
    response = client.post("/vote", json={"post_id": create_multiple_posts[0].id, "dir": 1})

    assert response.status_code == 401