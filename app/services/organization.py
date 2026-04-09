from typing import List, Sequence

from fastapi import HTTPException
from geoalchemy2.functions import ST_MakeEnvelope
from sqlalchemy.orm import Session

from app.db.models import Activity, Organization
from app.db.repositories.activity import ActivityRepository
from app.db.repositories.organization import OrganizationRepository


class OrganizationService:

    def __init__(self):
        self.repo = OrganizationRepository()
        self.activity_repo = ActivityRepository()

    def get_organization_by_id(self, db: Session, org_id: int) -> Organization:
        """Получает организацию по id"""
        org = self.repo.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="No data")
        return org

    def get_by_building(self, db: Session, building_id: int, limit: int, offset: int) -> Sequence[Organization]:
        """Получает список организаций в указанном здании (по id здания)"""
        return self.repo.get_by_building(db, building_id, limit, offset)

    def get_activity_with_children(self, db: Session, activity_id: int) -> List[int]:
        """Получает список id организаций с вложенностью по виду деятельности"""
        root = self.activity_repo.get_with_children(db, activity_id)
        if not root:
            return []

        result = []

        def collect(act: Activity) -> None:
            result.append(act.id)
            for child in act.children:
                collect(child)

        collect(root)
        return result

    def get_by_activity(
        self, db: Session, activity_id: int, include_children: bool, limit: int, offset: int
    ) -> Sequence[Organization]:
        """Получает список организаций с вложенностью по виду деятельности"""
        if include_children:
            activity_ids = self.get_activity_with_children(db, activity_id)
        else:
            activity_ids = [activity_id]
        if not activity_ids:
            return []
        return self.repo.get_by_activity(db, activity_ids, limit, offset)

    def get_in_radius(
        self, db: Session, lat: float, lon: float, radius_m: float, limit: int, offset: int
    ) -> Sequence[Organization]:
        """Получает список организаций в заданном радиусе на карте"""
        point = f"SRID=4326;POINT({lon} {lat})"
        return self.repo.get_in_radius(db, point, radius_m, limit, offset)

    def get_in_bbox(
        self, db: Session, min_lat: float, max_lat: float, min_lon: float, max_lon: float, limit: int, offset: int
    ) -> Sequence[Organization]:
        """Получает список организаций в заданном прямоугольной области на карте"""
        bbox = ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
        return self.repo.get_in_bbox(db, bbox, limit, offset)

    def get_by_name(self, db: Session, name: str, limit: int, offset: int) -> Sequence[Organization]:
        """Получает список организаций по наименованию"""
        return self.repo.get_by_name(db, name, limit, offset)
