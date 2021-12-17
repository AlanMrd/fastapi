from fastapi.exceptions import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends, status
from jose.exceptions import JWTError

from app.utils import verify
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import Settings

settings = Settings()
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentiais_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")

        if id is None:
            raise credentiais_exception

        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentiais_exception

    return token_data

def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validade credentials",
    headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)