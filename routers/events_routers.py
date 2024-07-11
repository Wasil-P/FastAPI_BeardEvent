from models.db import get_db
from .users_routers import manager
from models.schemas import User, Event, EventCreate, InvitationCreate
from controllers.events_crud import get_events_all, get_event_by_id, create_new_event

from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter()


@router.get("/", response_model=List[Event], status_code=200)
def read_events_all(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    events = get_events_all(db=db, skip=skip, limit=limit)
    return events


@router.get("/{id}", response_model=Event, status_code=200)
def get_event(id: int, db: Session = Depends(get_db)):
    event = get_event_by_id(db=db, id=id)
    return event


@router.get("/author", response_model=List[Event])
def get_events_author():
    pass


@router.post("/author", response_model=EventCreate)
def create_event(event: EventCreate, db: Session = Depends(get_db), user: User = Depends(manager)):
    new_event = create_new_event(db=db, event=event, user=user)
    return new_event


@router.get("/author/{id}", response_model=Event)
def get_my_event(id: int):
    pass


@router.post("/author/{id}", response_model=InvitationCreate)
def send_invitation(id: int):

    """The functionality of inviting all participants at once,
    or each participant separately, has been implemented."""
    pass