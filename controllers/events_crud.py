from models.model import Event
from models.schemas import Event, EventCreate

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST
