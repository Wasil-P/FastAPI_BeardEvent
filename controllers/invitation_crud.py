from models.model import Invitation as InvitationModel
from models.schemas import User, InvitationCreate

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_invitation_by_id(db: AsyncSession, id: int):
    invitation = await db.execute(select(InvitationModel).filter(InvitationModel.id == id))
    return invitation.scalars().first()


async def get_invitation_by_user(db: AsyncSession, invited_id: int):
    invitation_by_user = await (db.execute(select(InvitationModel).
                          filter(InvitationModel.invited_id == invited_id)))
    return invitation_by_user.scalars().first()


async def create_invitation(db: AsyncSession,
                      event_id: int,
                      user: User,
                      invitation: InvitationCreate,
                      invited_id: int):
    db_invitation = InvitationModel(
        name=invitation.name,
        event_id=event_id,
        inviter_id=user.id,
        invited_id=invited_id,
    )
    db.add(db_invitation)
    await db.commit()
    await db.refresh(db_invitation)

    return db_invitation
