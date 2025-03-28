from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from .base import Base


class DbUser(Base):
    __tablename__ = 'users'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = Column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = Column(String, nullable=False)
