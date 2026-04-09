from typing import Sequence

from geoalchemy2 import Geography
from geoalchemy2.functions import ST_DWithin, ST_Within
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Activity, Building, Organization


class OrganizationRepository:

    def _base_query(self):
        return select(Organization).options(
            joinedload(Organization.building), joinedload(Organization.phones), joinedload(Organization.activities)
        )

    def get_by_id(self, db: Session, org_id: int) -> Organization:
        """
        SQL-запрос: выбирает организацию по id
        Args:
            db: SQLAlchemy Session
            org_id: id организации
        Returns:
            Organization ORM объект
        """
        query = self._base_query().where(Organization.id == org_id)
        return db.scalars(query).first()

    def get_by_building(self, db: Session, building_id: int, limit: int, offset: int) -> Sequence[Organization]:
        """
        SQL-запрос: выбирает организации по id здания
        Args:
            db: SQLAlchemy Session
            building_id: id здания
            limit: количество записей
            offset: смещение
        Returns:
            Список Organization ORM объектов
        """
        query = (
            self._base_query()
            .where(Organization.building_id == building_id)
            .order_by(Organization.name)
            .limit(limit)
            .offset(offset)
        )
        return db.scalars(query).all()

    def get_by_activity(self, db: Session, activity_ids: list, limit: int, offset: int) -> Sequence[Organization]:
        """
        SQL-запрос: выбирает организации с вложенностью по виду деятельности
        Args:
            db: SQLAlchemy Session
            activity_ids: список id деятельности
            limit: количество записей
            offset: смещение
        Returns:
            Список Organization ORM объектов
        """
        query = (
            self._base_query()
            .join(Organization.activities)
            .where(Activity.id.in_(activity_ids))
            .distinct()
            .limit(limit)
            .offset(offset)
        )
        return db.scalars(query).all()

    def get_in_radius(
        self, db: Session, point: str, radius_m: float, limit: int, offset: int
    ) -> Sequence[Organization]:
        """
        SQL-запрос: выбирает организации в заданном радиусе на карте
        Args:
            db: SQLAlchemy Session
            point: точка (геопозиция) на карте
            radius_m: радиус
            limit: количество записей
            offset: смещение
        Returns:
            Список Organization ORM объектов
        """
        query = (
            self._base_query()
            .join(Organization.building)
            .where(ST_DWithin(Building.location.cast(Geography), func.ST_GeogFromText(point), radius_m))
            .limit(limit)
            .offset(offset)
        )
        return db.scalars(query).all()

    def get_in_bbox(self, db: Session, bbox, limit: int, offset: int) -> Sequence[Organization]:
        """
        SQL-запрос: выбирает организации в заданном прямоугольной области на карте
        Args:
            db: SQLAlchemy Session
            bbox: прямоугольная область
            limit: количество записей
            offset: смещение
        Returns:
            Список Organization ORM объектов
        """
        query = (
            self._base_query()
            .join(Organization.building)
            .where(ST_Within(Building.location, bbox))
            .limit(limit)
            .offset(offset)
        )
        return db.scalars(query).all()

    def get_by_name(self, db: Session, name: str, limit: int, offset: int) -> Sequence[Organization]:
        """
        SQL-запрос: выбирает организации по наименованию
        Args:
            db: SQLAlchemy Session
            name: наименование организации
        Returns:
            Список Organization ORM объектов
        """
        query = self._base_query().where(Organization.name.ilike(f"%{name}%")).limit(limit).offset(offset)
        return db.scalars(query).all()
