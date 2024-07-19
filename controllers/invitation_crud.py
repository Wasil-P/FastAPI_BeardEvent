from models.model import Invitation as InvitationModel
from models.schemas import User, InvitationCreate

from sqlalchemy.orm import Session



def get_invitation_by_id(db: Session, id: int):
    invitation = db.query(InvitationModel).filter(InvitationModel.id == id).first()
    return invitation


def get_invitation_by_user(db: Session, invited_id: int):
    invitation_by_user = (db.query(InvitationModel).
                          filter(InvitationModel.invited_id == invited_id).
                          first())
    return invitation_by_user


def create_invitation(db: Session,
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
    db.commit()
    db.refresh(db_invitation)

    return db_invitation
