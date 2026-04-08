from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(ForeignKey("activities.id"), nullable=True)
    level = Column(Integer, default=0, nullable=False)

    parent = relationship("Activity", remote_side=[id], backref="children")
    organizations = relationship(
        "Organization",
        secondary="organization_activity",
        back_populates="activities",
    )
