from models.model import User
from models.schemas import UserCreate

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from passlib.context import CryptContext
from starlette.status import HTTP_400_BAD_REQUEST


pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)


def get_users(db: Session, skip: int = 0, limit: int = 20):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


def get_user(db: Session, id:  int):
    return db.query(User).filter(User.id == id).first()


def get_user_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):

    if get_user_username(db=db, username=user.username):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST
                            , detail='Username already registered')
    if get_user_by_email(db=db, email=user.email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Email already registered')

    hash_password = get_hashed_password(user.password)
    db_user = User(
        username=user.username,
        phone=user.phone,
        email=user.email,
        password=hash_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def authenticate_user(username: str, password: str, db: Session):
    user = get_user_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST
                            , detail='This user does not exist!')
    if not verify_password(plain_password=password, hashed_password=user.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST
                            , detail='Wrong password!')
    return user

