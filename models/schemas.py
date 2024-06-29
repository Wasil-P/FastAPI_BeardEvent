from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from model import StatusEnum


class UserBase(BaseModel):
    username: str
    email: str
    password: str
    phone: str | None = None
    notice: bool


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class EventBase(BaseModel):
    name: str
    event_date: datetime
    place: str
    about: str


class Event(EventBase):
    id: int
    date_creation: datetime = datetime.now()
    author: User


class InvitationBase(BaseModel):
    name: str


class Invitation(InvitationBase):
    id: int
    event: Event
    inviter: User
    invited: User
    status: StatusEnum = Field(default=StatusEnum.NO_RESPONSE)
