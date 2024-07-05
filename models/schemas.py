from .model import StatusEnum

from pydantic import BaseModel, Field
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: str
    phone: str | None = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    notice: bool = Field(default=True)


class EventBase(BaseModel):
    name: str
    author: User
    date_creation: datetime = datetime.now()
    event_date: datetime
    place: str
    about: str


class Event(EventBase):
    id: int

    class Config:
        from_attributes = True


class EventCreate(EventBase):
    pass


class InvitationBase(BaseModel):
    name: str
    event: Event
    inviter: User
    invited: User
    status: StatusEnum = Field(default=StatusEnum.NO_RESPONSE)


class Invitation(InvitationBase):
    id: int

    class Config:
        from_attributes = True


class InvitationCreate(InvitationBase):
    pass