from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends

from models.db import get_db
from routers.users_routers import manager
from models.schemas import (
    User,
    Event,
    EventCreate,
    InvitationCreate,
    SMTPSettings)
from controllers.events_crud import (
    get_events_all,
    get_event_by_id,
    create_new_event,
    get_events_author_by_user)
from controllers.invitation_crud import create_invitation, get_invitation_by_user
from controllers.users_crud import get_user_username, get_user
from controllers.email_sender import send_email_invitation
from controllers.telegram_sender import send_message_tg

router = APIRouter()


@router.get("/", response_model=List[Event], status_code=200)
async def read_events_all(db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 10):
    events = await get_events_all(db=db, skip=skip, limit=limit)
    return events


@router.get("/{ev_id}", response_model=Event, status_code=200)
async def get_event(ev_id: int, db: AsyncSession = Depends(get_db)):
    event = await get_event_by_id(db=db, id=ev_id)
    return event


@router.post("/{ev_id}", response_model=InvitationCreate, status_code=201)
async def send_invitation_from_user_request(invitation: InvitationCreate,
                                      ev_id: int,
                                      smtp_settings: SMTPSettings,
                                      db: AsyncSession = Depends(get_db),
                                      user: User = Depends(manager)):
    if not user:
        return JSONResponse(status_code=401,
                            content={"detail": "Not authenticated"})

    user_from_db = get_user(db=db, id=invitation.invited_id)
    if not user_from_db:
        return JSONResponse(status_code=400,
                            content={"detail": "This user does not exist"})

    invitation_from_db = get_invitation_by_user(db=db,
                                                invited_id=invitation.invited_id)
    if invitation_from_db:
        return JSONResponse(status_code=400,
                            content={"detail": "This user has already been invited"})

    new_invitation = create_invitation(
        db=db,
        event_id=ev_id,
        user=user,
        invitation=invitation,
        invited_id=invitation.invited_id,
    )

    if not new_invitation:
        return JSONResponse(status_code=401, content={"detail": "Invitation not send"})
    invited_user = get_user(db=db, id=invitation.invited_id)
    send_email_invitation(
        inviter_user=user,
        invited_user=invited_user,
        invitation=new_invitation,
        smtp_email=user.email,
        smtp_password=smtp_settings.smtp_password,
        db=db,
    )
    tg_id = invited_user.tg_id
    if tg_id:
        event = get_event_by_id(db=db, id=ev_id)
        await send_message_tg(
            tg_id=tg_id,
            inviter=user.username,
            event=event,
            invitation=new_invitation,
        )

    return new_invitation


@router.get("/author/my_events", response_model=List[Event], status_code=200)
async def get_events_author(db: AsyncSession = Depends(get_db),
                      user: User = Depends(manager)):
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})
    events = await get_events_author_by_user(db=db, user_id=user.id)
    return events


@router.post("/author/my_events", response_model=EventCreate, status_code=201)
async def create_event(event: EventCreate,
                 db: AsyncSession = Depends(get_db),
                 user: User = Depends(manager)):
    new_event = await create_new_event(db=db, event=event, user=user)
    return new_event


@router.get("/author/my_events/{ev_id}", response_model=Event, status_code=200)
async def get_event(ev_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(manager)):
    event = await get_event_by_id(db=db, id=ev_id)
    owner_id = event.author_id
    if owner_id == user.id:
        return event
    return JSONResponse(status_code=401, content={"detail": "You are not the owner"})


@router.post("/author/my_events/{ev_id}", response_model=List[InvitationCreate], status_code=201)
async def send_invitation_from_owner(invitation: InvitationCreate,
                               ev_id: int,
                               usernames: List[str],
                               smtp_settings: SMTPSettings,
                               db: AsyncSession = Depends(get_db),
                               user: User = Depends(manager),
                               ):
    if not user:
        return JSONResponse(status_code=401, content={"detail": "Not authenticated"})

    list_users = [get_user_username(db, username) for username in usernames]
    new_invitation_list = []

    for user_from_list in list_users:
        new_invitation = create_invitation(
            db=db,
            event_id=ev_id,
            user=user,
            invitation=invitation,
            invited_id=user_from_list.id)

        if not new_invitation:
            return JSONResponse(status_code=401, content={"detail": "Invitation not send"})

        send_email_invitation(
            inviter_user=user,
            invited_user=user_from_list,
            invitation=new_invitation,
            smtp_email=user.email,
            smtp_password=smtp_settings.smtp_password,
            db=db,
        )
        tg_id = user_from_list.tg_id
        if tg_id:
            event = get_event_by_id(db=db, id=ev_id)
            await send_message_tg(
                tg_id=tg_id,
                inviter=user.username,
                event=event,
                invitation=new_invitation,
            )
        new_invitation_list.append(new_invitation)

    return [InvitationCreate.from_orm(invitation) for invitation in new_invitation_list]
