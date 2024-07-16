from models.db import get_db, DBContext
from models.schemas import User, UserCreate, UserLogin
from controllers.users_crud import (
                    get_user_username,
                    get_users,
                    create_user,
                    authenticate_user)

import os
from dotenv import load_dotenv
from datetime import timedelta
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_login import LoginManager
from fastapi.responses import JSONResponse

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set for LoginManager")
manager = LoginManager(os.getenv("SECRET_KEY"), token_url="/users/login", use_cookie=True)
manager.cookie_name = "auth"

router = APIRouter()


@manager.user_loader()
def get_user(username: str, db: Session = None):
    if db is None:
        with DBContext() as db:
            return get_user_username(db=db, username=username)
    return get_user_username(db=db, username=username)


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = get_users(db, skip, limit)
    return users


@router.post("/register", response_model=UserCreate)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    create_user(db=db, user=user)
    response = JSONResponse({"message": "Login successful"}, status_code=201)
    return response


@router.post("/login")
def login(login_request: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(username=login_request.username,
                             password=login_request.password,
                             db=db)
    access_token_expires = timedelta(minutes=int(os.getenv("ACCESS_T_MIN")))
    access_token = manager.create_access_token(
        data={"sub": user.username},
        expires=access_token_expires
    )
    response = JSONResponse({"message": "Login successful"}, status_code=200)
    manager.set_cookie(response, access_token)
    return response


@router.get("/logout")
def logout():
    response = JSONResponse({"message": "Logout successful"}, status_code=200)
    manager.set_cookie(response, None)
    return response
