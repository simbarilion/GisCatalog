from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.models.base import Base


class Phone(Base):
    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    organization_id = Column(ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="phones")
