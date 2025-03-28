from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.users import DbUser


def get_user_by_email(db: Session, email: str) -> Optional[DbUser]:
    stmt = select(DbUser).where(DbUser.email == email)
    return db.scalar(stmt)


def create_user(
        db: Session,
        email: str,
        hashed_password: str
) -> DbUser:
    db_user = DbUser(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
