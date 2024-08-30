from models.model import User
from models.schemas import UserCreate

import asyncio
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from passlib.context import CryptContext
from starlette.status import HTTP_400_BAD_REQUEST



pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)


def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)


async def get_users(db: AsyncSession, skip: int = 0, limit: int = 20):
    users = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    return users.scalars().all()


async def get_user(db: AsyncSession, id:  int):
    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()


async def get_user_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: UserCreate):

    if await get_user_username(db=db, username=user.username):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST
                            , detail='Username already registered')
    if await get_user_by_email(db=db, email=user.email):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST,
                            detail='Email already registered')

    hash_password = get_hashed_password(user.password)
    db_user = User(
        username=user.username,
        phone=user.phone,
        email=user.email,
        password=hash_password,
        notice=user.notice,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def authenticate_user(username: str, password: str, db: AsyncSession):
    user = await get_user_username(db=db, username=username)
    if not user:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST
                            , detail='This user does not exist!')
    if not verify_password(plain_password=password, hashed_password=user.password):
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST
                            , detail='Wrong password!')
    return user


async def get_list_user_notice(db: AsyncSession, user_id: int):
    list_user_notice = await (db.execute(select(User).
                        filter(User.notice == True,  User.id != user_id)))
    return list_user_notice.scalars().all()


