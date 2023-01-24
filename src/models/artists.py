from sqlalchemy import Column, String

from src.models.base import Base


class Artists(Base):
    __tablename__ = "artists"

    uri = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
