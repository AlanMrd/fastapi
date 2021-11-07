from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel, main
from random import randrange
import psycopg2

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [{"title": "title of post 1", "content": "content of post1", "id": "1"},
            {"title": "title of post 2", "content": "content of post2", "id": "2"}]

conn = psycopg2.connect(host="localhost", dbname="fastapi", user="postgres", password="123456")
cursor = conn.cursor()

def find_post(id):
    for post in my_posts:
        if id == post["id"]:
            return post

def find_post_index(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
            break

app = FastAPI() 

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}

@app.get("/posts/{id}")
def get_post(id):
    cursor.execute("SELECT * FROM posts WHERE id = %s;", [id])
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"The post {id} was not found")
    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *", (post.title, post.content))
    new_post = cursor.fetchone()
    
    conn.commit()
    return {"data": new_post}

@app.delete("/posts/{id}")
def delete_post(id):
    cursor.execute("DELETE FROM posts WHERE id = %s returning *" , (id))
    deleted_post = cursor.fetchone()
 
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} doesn't exist")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} was not found")

    conn.commit()
    return {"message": f"The post {id} was updated"}
