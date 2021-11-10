from fastapi import APIRouter, Response, status, HTTPException
from app import models, schemas
from app.utils import pwd_context
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
from app.database import engine, get_db
from typing import List

router = APIRouter(tags=["Posts"])

@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/posts/{id}", response_model=schemas.Post)
def get_post(id, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"The post {id} was not found")
    return post

@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.delete("/posts/{id}")
def delete_post(id, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
 
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} doesn't exist")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schemas.Post)
def update_post(id, post: schemas.PostCreate, db: Session = Depends(get_db)):
    query_post = db.query(models.Post).filter(models.Post.id == id)
    updated_post = query_post.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post {id} was not found")

    query_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post
