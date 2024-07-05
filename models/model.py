from enum import Enum
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String, index=True, unique=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String)
    notice = Column(Boolean, default=True)

    events = relationship("Event", back_populates="author")
    invitations_sent = relationship("Invitation", foreign_keys='Invitation.inviter_id', back_populates="inviter")
    invitations_received = relationship("Invitation", foreign_keys='Invitation.invited_id', back_populates="invited")


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    date_creation = Column(DateTime, default=datetime.now)
    event_date = Column(DateTime)
    place = Column(String, nullable=False)
    about = Column(String)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    author = relationship("User", back_populates="events")
    invitations = relationship("Invitation", back_populates="events")


class StatusEnum(str, Enum):
    CONFIRMED = 'confirmed participation'
    DECLINED = 'declined'
    NO_RESPONSE = 'did not respond'


class Invitation(Base):
    __tablename__ = 'invitations'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    event = Column(Integer, ForeignKey('events.id'), nullable=False)
    inviter_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    invited_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, default=StatusEnum.NO_RESPONSE.value)

    events = relationship("Event", back_populates="invitations")
    inviter = relationship("User", foreign_keys=[inviter_id], back_populates="invitations_sent")
    invited = relationship("User", foreign_keys=[invited_id], back_populates="invitations_received")
