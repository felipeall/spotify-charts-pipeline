from sqlalchemy import Column, INTEGER, VARCHAR

from src.models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(64))
