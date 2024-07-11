from models.schemas import Event, EventCreate, InvitationCreate

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status




router = APIRouter()


@router.get("/", response_model=List[Event])
def get_events_all():
    pass


@router.get("/{id}", response_model=Event)
def get_event(id: int):
    pass


@router.get("/author", response_model=List[Event])
def get_events_author():
    pass


@router.post("/author", response_model=EventCreate)
def create_event():
    pass


@router.get("/author/{id}", response_model=Event)
def get_my_event(id: int):
    pass


@router.post("/author/{id}", response_model=InvitationCreate)
def send_invitation(id: int):

    """The functionality of inviting all participants at once,
    or each participant separately, has been implemented."""
    pass