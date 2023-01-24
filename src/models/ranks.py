from sqlalchemy import Column, Date, Integer, String

from src.models.base import Base


class Ranks(Base):
    __tablename__ = "ranks"

    chartUri = Column(String, nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True)
    trackUri = Column(String, nullable=False)
    currentRank = Column(Integer, nullable=False, primary_key=True)
    previousRank = Column(Integer, nullable=False)
    peakRank = Column(Integer, nullable=False)
    appearancesOnChart = Column(Integer, nullable=False)
    consecutiveAppearancesOnChart = Column(Integer, nullable=False)
    metricValue = Column(Integer, nullable=False)
    metricType = Column(String, nullable=False)
    entryStatus = Column(String, nullable=False)
    peakDate = Column(Date, nullable=False)
    entryRank = Column(Integer, nullable=False)
    entryDate = Column(Date, nullable=False)
