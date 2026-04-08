from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Organization
from app.db.repositories.organization import OrganizationRepository


class OrganizationService:

    def __init__(self):
        self.repo = OrganizationRepository()

    def get_organization_by_id(self, db: Session, org_id: int) -> Organization:
        """Получает организацию по id"""
        org = self.repo.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="No data")
        return org
