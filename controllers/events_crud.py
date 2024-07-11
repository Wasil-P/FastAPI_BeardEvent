

from models.model import Event
from models.schemas import User, EventCreate

import datetime
from pytz import utc
from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from starlette.status import HTTP_400_BAD_REQUEST


def get_events_all(db: Session, skip: int = 0, limit: int = 10):
    events = (db.query(Event).
              filter(Event.event_date >= datetime.datetime.now()).
              offset(skip).limit(limit).
              all())
    return events


def get_event_by_id(db: Session, id: int):
    event = db.query(Event).filter(Event.id == id).first()
    return event


def create_new_event(db: Session, event: EventCreate, user: User):
    event_date = event.event_date.astimezone(utc)
    now = datetime.datetime.now().astimezone(utc)
    if event_date <= now:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST
                            , detail='This date is not valid')
    db_event = Event(
        name=event.name,
        event_date=event_date,
        place=event.place,
        about=event.about,
        author_id=user.id,
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event