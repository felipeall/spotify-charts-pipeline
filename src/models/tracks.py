from sqlalchemy import ARRAY, Column, Date, String, Unicode

from src.models.base import Base


class Tracks(Base):
    __tablename__ = "tracks"

    trackUri = Column(String, nullable=False, primary_key=True)
    trackName = Column(String, nullable=False)
    displayImageUri = Column(String, nullable=False)
    artistUri = Column(ARRAY(Unicode), nullable=False)
    labels = Column(ARRAY(Unicode), nullable=False)
    releaseDate = Column(Date, nullable=True)
