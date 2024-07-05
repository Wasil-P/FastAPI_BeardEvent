from models.model import User

from sqlalchemy.orm import Session


def get_users(db: Session, skip: int = 0, limit: int = 20):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
