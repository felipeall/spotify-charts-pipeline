from sqlalchemy import Column, Date, String

from src.models.base import Base


class Charts(Base):
    __tablename__ = "charts"

    uri = Column(String, nullable=False, primary_key=True)
    alias = Column(String, nullable=False)
    entityType = Column(String, nullable=False)
    readableTitle = Column(String, nullable=False)
    backgroundColor = Column(String, nullable=False)
    textColor = Column(String, nullable=False)
    latestDate = Column(Date, nullable=False)
    earliestDate = Column(Date, nullable=False)
    country = Column(String, nullable=False)
    chartType = Column(String, nullable=False)
    recurrence = Column(String, nullable=False)
