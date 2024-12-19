from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import Depends, HTTPException, status
from database import users_collection
from models import  TokenData
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    db_user = users_collection.find_one({"username" : token_data.username})
    if db_user is None:
        raise credentials_exception
    return db_user

def is_valid_date(date_string: str, date_formate: str =  "%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_formate)
        return True
    except ValueError:
        return False
    

