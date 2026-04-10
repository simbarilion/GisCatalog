from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.db.models import Activity


class ActivityRepository:

    def get_activity_ids_with_children(self, db: Session, activity_id: int) -> list[int]:
        """
        Рекурсивный CTE-запрос:
        возвращает список id всех вложенных видов деятельности (родитель + все потомки)
        Args:
            db: SQLAlchemy Session
            activity_id: id вида деятельности
        """
        query = text("""
                    WITH RECURSIVE activity_tree AS (
                        SELECT id, parent_id, level
                        FROM activities
                        WHERE id = :activity_id

                        UNION ALL

                        SELECT a.id, a.parent_id, a.level
                        FROM activities a
                                 INNER JOIN activity_tree at
                    ON a.parent_id = at.id
                        )
                    SELECT id
                    FROM activity_tree
                    ORDER BY level, id;
                    """)

        result = db.execute(query, {"activity_id": activity_id}).scalars().all()
        return list(result)

    def get_activity_by_id(self, db: Session, activity_id: int) -> Activity | None:
        """
        SQL-запрос: выбирает вид деятельности по id
        Args:
            db: SQLAlchemy Session
            activity_id: id вида деятельности
        Returns:
            Activity ORM объект or None
        """
        query = select(Activity).where(Activity.id == activity_id)
        return db.scalars(query).first()
