from geoalchemy2 import Geography
from geoalchemy2.functions import ST_X, ST_Y, ST_DWithin, ST_SetSRID, ST_Within
from sqlalchemy import exists, func, select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Building, Organization, organization_activity


class OrganizationRepository:

    def _base_query(self):
        """
        Вспомогательный SQL-запрос для данных: загружает данные из связанных таблиц одним запросом
        """
        return (
            select(
                Organization,
                ST_Y(Building.location).label("latitude"),
                ST_X(Building.location).label("longitude"),
            )
            .join(Organization.building)
            .options(
                joinedload(Organization.building), joinedload(Organization.phones), joinedload(Organization.activities)
            )
        )

    def _paginate(self, db: Session, data_query, count_query, limit: int, offset: int) -> tuple[list[dict], int]:
        """
        Универсальная пагинация. Вспомогательные SQL-запросы возвращают:
         - данные для любого запроса с пагинацией (items)
         - общее количество полученных данных (total)
        """
        rows = db.execute(data_query.limit(limit).offset(offset)).unique().all()
        items = [
            {
                "id": org.id,
                "name": org.name,
                "latitude": lat,
                "longitude": lon,
            }
            for org, lat, lon in rows
        ]
        total = db.scalar(count_query) or 0
        return items, total

    def get_organization_by_id(self, db: Session, org_id: int) -> Organization | None:
        """
        Выбирает организацию по id
        Args:
            db: SQLAlchemy Session
            org_id: id организации
        Returns:
            Organization ORM объект
        """
        query = self._base_query().where(Organization.id == org_id)
        return db.scalars(query).first()

    def get_by_name(self, db: Session, name: str, limit: int, offset: int) -> tuple[list[dict], int]:
        """
        Выбирает организации по наименованию
        Args:
            db: SQLAlchemy Session
            name: наименование организации
            limit: количество записей
            offset: смещение
        Returns:
            Кортеж: Коллекция Organization ORM объектов с пагинацией, общее количество Organization ORM объектов
        """
        data_query = self._base_query().where(Organization.name.ilike(f"%{name}%")).order_by(Organization.name)
        count_query = select(func.count()).select_from(Organization).where(Organization.name.ilike(f"%{name}%"))
        return self._paginate(db, data_query, count_query, limit, offset)

    def get_by_building(self, db: Session, building_id: int, limit: int, offset: int) -> tuple[list[dict], int]:
        """
        Выбирает организации по id здания
        Args:
            db: SQLAlchemy Session
            building_id: id здания
            limit: количество записей
            offset: смещение
        Returns:
            Кортеж: Коллекция Organization ORM объектов с пагинацией, общее количество Organization ORM объектов
        """
        data_query = self._base_query().where(Organization.building_id == building_id).order_by(Organization.name)
        count_query = select(func.count()).select_from(Organization).where(Organization.building_id == building_id)
        return self._paginate(db, data_query, count_query, limit, offset)

    def get_by_activity(self, db: Session, activity_ids: list, limit: int, offset: int) -> tuple[list[dict], int]:
        """
        Выбирает организации с вложенностью по виду деятельности
        Args:
            db: SQLAlchemy Session
            activity_ids: список id деятельности
            limit: количество записей
            offset: смещение
        Returns:
            Кортеж: Коллекция Organization ORM объектов с пагинацией, общее количество Organization ORM объектов
        """
        data_query = self._base_query().where(
            exists(
                select(1)
                .select_from(organization_activity)
                .where(
                    organization_activity.c.organization_id == Organization.id,
                    organization_activity.c.activity_id.in_(activity_ids),
                )
            )
        )
        count_query = (
            select(func.count())
            .select_from(Organization)
            .where(
                exists(
                    select(1)
                    .select_from(organization_activity)
                    .where(
                        organization_activity.c.organization_id == Organization.id,
                        organization_activity.c.activity_id.in_(activity_ids),
                    )
                )
            )
        )
        return self._paginate(db, data_query, count_query, limit, offset)

    def get_in_radius(
        self, db: Session, point: ST_SetSRID, radius_m: float, limit: int, offset: int
    ) -> tuple[list[dict], int]:
        """
        Выбирает организации в заданном радиусе на карте
        Args:
            db: SQLAlchemy Session
            point: точка (геопозиция) на карте
            radius_m: радиус
            limit: количество записей
            offset: смещение
        Returns:
            Кортеж: Коллекция Organization ORM объектов с пагинацией, общее количество Organization ORM объектов
        """
        data_query = (
            self._base_query()
            .join(Organization.building)
            .where(ST_DWithin(Building.location.cast(Geography), point.cast(Geography), radius_m))
            .order_by(Organization.name)
        )
        count_query = (
            select(func.count())
            .select_from(Organization)
            .join(Organization.building)
            .where(ST_DWithin(Building.location.cast(Geography), point.cast(Geography), radius_m))
        )
        return self._paginate(db, data_query, count_query, limit, offset)

    def get_in_bbox(self, db: Session, bbox, limit: int, offset: int) -> tuple[list[dict], int]:
        """
        Выбирает организации в заданной прямоугольной области на карте
        Args:
            db: SQLAlchemy Session
            bbox: прямоугольная область
            limit: количество записей
            offset: смещение
        Returns:
            Кортеж: Коллекция Organization ORM объектов с пагинацией, общее количество Organization ORM объектов
        """
        data_query = (
            self._base_query()
            .join(Organization.building)
            .where(ST_Within(Building.location, bbox))
            .order_by(Organization.name)
        )
        count_query = (
            select(func.count())
            .select_from(Organization)
            .join(Organization.building)
            .where(ST_Within(Building.location, bbox))
        )
        return self._paginate(db, data_query, count_query, limit, offset)
