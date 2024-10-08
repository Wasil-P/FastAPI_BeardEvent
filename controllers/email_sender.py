import yagmail
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

from models.schemas import User, Invitation
from controllers.events_crud import get_event_by_id


async def send_email_invitation(
    inviter_user: User, 
    invited_user: User, 
    invitation: Invitation, 
    smtp_email: str,
    smtp_password: str,
    db: AsyncSession
):

    yag = yagmail.SMTP(smtp_email, smtp_password)
    try:
        event = await get_event_by_id(db, invitation.event_id)
    except Exception:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail='There is no such event.'
        )

    subject = f"Invitation to an event: {event.name}"
    body = f"""
    Hello, {invited_user.username}!

    You have been invited to an event "{event.name}".

    Event details:
    - From whom: {inviter_user.username}
    - About the event: {event.about}
    - Location: {event.place}
    - Date and time: {event.event_date.strftime('%Y-%m-%d %H:%M')}
    """

    try:
        yag.send(to=invited_user.email, subject=subject, contents=body)
    except Exception:
        raise HTTPException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error sending email'
        )