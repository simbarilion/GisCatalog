from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db.models import Activity


class ActivityRepository:

    def get_with_children(self, db: Session, activity_id: int) -> Activity | None:
        """
        SQL-запрос: выбирает вложенный вид деятельности
        Args:
            db: SQLAlchemy Session
            activity_id: id вида деятельности
        Returns:
            Activity ORM объект
        """
        query = (
            select(Activity)
            .options(joinedload(Activity.children).joinedload(Activity.children))
            .where(Activity.id == activity_id)
        )
        return db.scalars(query).first()

    def get_activity_by_id(self, db: Session, activity_id: int) -> Activity | None:
        """
        SQL-запрос: выбирает вид деятельности по id
        Args:
            db: SQLAlchemy Session
            activity_id: id вида деятельности
        Returns:
            Activity ORM объект
        """
        query = select(Activity).where(Activity.id == activity_id)
        return db.scalars(query).first()
