from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm.session import Session
from app.database import get_db
from .. import models, schemas, utils, oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user {user_credentials.email} doesn't exist")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The password is wrong")

    access_token = oauth2.create_acess_token(data={"user_id": user.id})
    
    return {"token": access_token, "token_type": "bearer"}