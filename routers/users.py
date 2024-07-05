from controllers.users import get_users
from models.db import get_db
from models.schemas import User

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    users = get_users(db, skip, limit)
    return users
