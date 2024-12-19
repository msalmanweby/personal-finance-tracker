from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import Depends, APIRouter, HTTPException, status
from database import users_collection
from models import User
import hashlib
import jwt
from utils import get_current_user

auth_router = APIRouter()
SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def regsiter(user : User):
    if users_collection.find_one({"username" : user.username}):
        raise HTTPException(status_code=400, detail={"message" : "User already exsist"})
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    user_data = {"username" : user.username, "password" : hashed_password}
    users_collection.insert_one(user_data)
    return {"message" : "User created successfully"}
    

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user : User):
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    db_user = users_collection.find_one({"username" : user.username, "password" : hashed_password})

    if not db_user:
        raise HTTPException(status_code=404, detail={"message" : "Invalid Credentials"})
    
    token  = jwt.encode({"username" : user.username}, SECRET_KEY, algorithm=ALGORITHM)
    return {"token" : token}


@auth_router.get("/profile", status_code=status.HTTP_200_OK)
async def profile(user: str = Depends(get_current_user)):
    return {
        "user_id" : str(user["_id"]),
        "username" : user["username"]
    }