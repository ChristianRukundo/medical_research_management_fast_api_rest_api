from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from ..config.database import Base


class Research(Base):
    __tablename__ = "researches"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    cost = Column(Float)
    duration_in_days = Column(Integer)
    category = Column(String, index=True)
    is_published = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    creator_id = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="researches")
