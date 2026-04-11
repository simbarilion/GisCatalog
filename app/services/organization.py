from typing import List

from geoalchemy2.functions import ST_MakeEnvelope, ST_MakePoint, ST_SetSRID
from sqlalchemy.orm import Session

from app.core.logging import setup_logger
from app.db.repositories.activity import ActivityRepository
from app.db.repositories.organization import OrganizationRepository
from app.mappers.organization import map_organization
from app.schemas.response import OrganizationListResponse

logger = setup_logger(__name__, level="WARNING")


class OrganizationService:

    def __init__(self):
        self.repo = OrganizationRepository()
        self.activity_repo = ActivityRepository()

    @staticmethod
    def _base_response(orgs, total: int, limit: int, offset: int) -> OrganizationListResponse:
        """Возвращает список организаций с пагинацией"""
        page = (offset // limit) + 1 if limit > 0 else 1
        return OrganizationListResponse(
            items=orgs,
            total=total,
            page=page,
            size=limit,
        )

    def get_organization_by_id(self, db: Session, org_id: int) -> dict:
        """Получает полную информацию об организации по id, возвращает в виде словаря значений"""
        org = self.repo.get_organization_by_id(db, org_id)
        if not org:
            logger.error("Поиск по id организации: %s. Организация не найдена", org_id)
            raise ValueError("Not found")
        logger.debug("Поиск по id организации: %s. Информация получена", org_id)
        return map_organization(org)

    def get_by_name(self, db: Session, name: str, limit: int, offset: int) -> OrganizationListResponse:
        """Получает список организаций по наименованию"""
        orgs, total = self.repo.get_by_name(db, name, limit, offset)
        logger.debug("Поиск по наименованию: %s. Получено %s организаций", name, total)
        return self._base_response(orgs, total, limit, offset)

    def get_by_building(self, db: Session, building_id: int, limit: int, offset: int) -> OrganizationListResponse:
        """Получает список организаций в указанном здании (по id здания)"""
        orgs, total = self.repo.get_by_building(db, building_id, limit, offset)
        logger.debug("Поиск по id здания: %s. Получено %s организаций", building_id, total)
        return self._base_response(orgs, total, limit, offset)

    def get_activity_with_children(self, db: Session, activity_id: int) -> List[int]:
        """Получает список id вида деятельности и всех его потомков"""
        return self.activity_repo.get_activity_ids_with_children(db, activity_id)

    def get_by_activity(self, db: Session, activity_id: int, limit: int, offset: int) -> OrganizationListResponse:
        """Получает список организаций с вложенностью по виду деятельности"""
        activity_ids = self.get_activity_with_children(db, activity_id)
        if not activity_ids:
            logger.warning("Поиск по id деятельности: %s. Организации не найдены", activity_id)
            return self._base_response([], 0, limit, offset)
        orgs, total = self.repo.get_by_activity(db, activity_ids, limit, offset)
        logger.debug("Поиск по id деятельности: %s. Получено %s организаций", activity_id, total)
        return self._base_response(orgs, total, limit, offset)

    def get_in_radius(
        self, db: Session, lat: float, lon: float, radius_m: float, limit: int, offset: int
    ) -> OrganizationListResponse:
        """Получает список организаций в заданном радиусе на карте"""
        point = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
        orgs, total = self.repo.get_in_radius(db, point, radius_m, limit, offset)
        logger.debug("Поиск по геопозиции: %s, %s (радиус: %s). Получено %s организаций", lat, lon, radius_m, total)
        return self._base_response(orgs, total, limit, offset)

    def get_in_bbox(
        self, db: Session, min_lat: float, max_lat: float, min_lon: float, max_lon: float, limit: int, offset: int
    ) -> OrganizationListResponse:
        """Получает список организаций в заданной прямоугольной области на карте"""
        bbox = ST_MakeEnvelope(min_lon, min_lat, max_lon, max_lat, 4326)
        orgs, total = self.repo.get_in_bbox(db, bbox, limit, offset)
        logger.debug(
            "Поиск по геопозиции: %s-%s / %s-%s. Получено %s организаций", min_lat, max_lat, min_lon, max_lon, total
        )
        return self._base_response(orgs, total, limit, offset)
