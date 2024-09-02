from models.model import Event
from models.schemas import User, EventCreate

import datetime
from pytz import utc
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


async def get_events_all(db: AsyncSession, skip: int = 0, limit: int = 10):
    events = await (db.execute(select(Event).
              filter(Event.event_date >= datetime.datetime.now()).
              offset(skip).limit(limit)))
    return events.scalars().all()


async def get_event_by_id(db: AsyncSession, id: int):
    event = await db.execute(select(Event).filter(Event.id == id))
    return event.scalars().first()


async def get_events_author_by_user(db: AsyncSession, user_id: int):
    events = await db.execute(select(Event).filter(Event.author_id == user_id))
    return events.scalars().all()


async def create_new_event(db: AsyncSession, event: EventCreate, user: User):
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
    await db.commit()
    await db.refresh(db_event)

    return db_event