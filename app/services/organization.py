from typing import List

from geoalchemy2.functions import ST_MakeEnvelope, ST_MakePoint, ST_SetSRID
from sqlalchemy.orm import Session

from app.db.models import Organization
from app.db.repositories.activity import ActivityRepository
from app.db.repositories.organization import OrganizationRepository
from app.schemas.response import OrganizationListResponse


class OrganizationService:

    def __init__(self):
        self.repo = OrganizationRepository()
        self.activity_repo = ActivityRepository()

    @staticmethod
    def _base_response(orgs, total: int, limit: int, offset: int) -> OrganizationListResponse:
        """Возвращает список организаций"""
        page = (offset // limit) + 1 if limit > 0 else 1
        return OrganizationListResponse(
            items=orgs,
            total=total,
            page=page,
            size=limit,
        )

    def get_organization_by_id(self, db: Session, org_id: int) -> Organization:
        """Получает организацию по id"""
        org = self.repo.get_organization_by_id(db, org_id)
        if not org:
            raise ValueError("Not found")
        return org

    def get_by_building(self, db: Session, building_id: int, limit: int, offset: int) -> OrganizationListResponse:
        """Получает список организаций в указанном здании (по id здания)"""
        orgs, total = self.repo.get_by_building(db, building_id, limit, offset)
        return self._base_response(orgs, total, limit, offset)

    def get_activity_with_children(self, db: Session, activity_id: int) -> List[int]:
        """Получает список id вида деятельности и всех его потомков"""
        return self.activity_repo.get_activity_ids_with_children(db, activity_id)

    def get_by_activity(
        self, db: Session, activity_id: int, include_children: bool, limit: int, offset: int
    ) -> OrganizationListResponse:
        """Получает список организаций с вложенностью по виду деятельности"""
        if include_children:
            activity_ids = self.get_activity_with_children(db, activity_id)
        else:
            activity_ids = [activity_id]
        if not activity_ids:
            return self._base_response([], 0, limit, offset)
        orgs, total = self.repo.get_by_activity(db, activity_ids, limit, offset)
        return self._base_response(orgs, total, limit, offset)

    def get_in_radius(
        self, db: Session, lat: float, lon: float, radius_m: float, limit: int, offset: int
    ) -> OrganizationListResponse:
        """Получает список организаций в заданном радиусе на карте"""
        point = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
        orgs, total = self.repo.get_in_radius(db, point, radius_m, limit, offset)
        return self._base_response(orgs, total, limit, offset)

    def get_in_bbox(
        self, db: Session, min_lat: float, max_lat: float, min_lon: float, max_lon: float, limit: int, offset: int
    ) -> OrganizationListResponse:
        """Получает список организаций в заданной прямоугольной области на карте"""
        bbox = ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
        orgs, total = self.repo.get_in_bbox(db, bbox, limit, offset)
        return self._base_response(orgs, total, limit, offset)

    def get_by_name(self, db: Session, name: str, limit: int, offset: int) -> OrganizationListResponse:
        """Получает список организаций по наименованию"""
        orgs, total = self.repo.get_by_name(db, name, limit, offset)
        return self._base_response(orgs, total, limit, offset)
