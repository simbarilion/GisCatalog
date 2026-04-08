from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Organization


class OrganizationRepository:

    def get_by_id(self, db: Session, org_id: int) -> Organization:
        """
        SQL-запрос: выбирает организацию по id
        Args:
            db: SQLAlchemy Session
            org_id: id организации
        Returns:
            Organization ORM объект
        """
        query = select(Organization).where(Organization.id == org_id)
        return db.scalars(query).first()
