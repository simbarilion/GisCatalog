from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    building_id = Column(ForeignKey("buildings.id"), nullable=False)

    building = relationship("Building", back_populates="organizations")

    phones = relationship(
        "Phone",
        back_populates="organization",
        cascade="all, delete-orphan",
    )

    activities = relationship(
        "Activity",
        secondary="organization_activity",
        back_populates="organizations",
    )
