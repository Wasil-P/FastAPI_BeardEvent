import yagmail
from datetime import datetime, timedelta
from celery import shared_task
from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from models.model import Event, Invitation, User
from models.db import get_db, DBContext


@shared_task(ignore_result=True)
def event_reminder(smtp_email: str, smtp_password: str, ):
    with DBContext() as db:
        try:
            events = db.query(Event).filter(Event.event_date > datetime.now()).all()
            for event in events:
                if event.event_date.date() == ((datetime.now() +
                                                timedelta(days=1)).
                                                date()):
                    user_invitations = (db.query(Invitation).
                                        filter(Invitation.event_id == event.id).
                                        all())

                    yag = yagmail.SMTP(smtp_email, smtp_password)

                    for invitation in user_invitations:
                        user = (db.query(User).
                                filter(User.id == invitation.invited_id).
                                first())

                        subject = f"Coming soon {event.name}"
                        body = f"""
                            Hello, {user.username}!

                            "{event.name}" will take place very soon.
                            Event details:
                            - Location: {event.place}
                            - Date and time: {event.event_date.strftime('%Y-%m-%d %H:%M')}
                            """

                        try:
                            yag.send(to=user.email, subject=subject, contents=body)
                        except Exception as e:
                            raise HTTPException(
                                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f'Error sending email: {str(e)}'
                            )
        except Exception as e:
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Error processing event reminders: {str(e)}'
            )
