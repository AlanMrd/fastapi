from fastapi import APIRouter, Response, status, HTTPException
from app import models, schemas
from app.utils import pwd_context
from sqlalchemy.orm.session import Session
from fastapi.params import Depends
from app.database import engine, get_db

router = APIRouter(tags=["Users"])

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {id} doesn't exist")

    return user