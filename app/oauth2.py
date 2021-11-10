from jose import JWSError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "2cfe3f70f7daf95bdbd75fbc5facdd5e5932bc25d233e623732e7a1f5a419052"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acess_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt