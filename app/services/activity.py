from sqlalchemy.orm import Session

from app.core.logging import setup_logger
from app.db.models import Activity
from app.db.repositories.activity import ActivityRepository

logger = setup_logger(__name__, level="INFO")


class ActivityService:
    MAX_LEVEL = 3

    def __init__(self):
        self.repo = ActivityRepository()

    def create_activity(self, db: Session, name: str, parent_id: int | None) -> Activity:
        """
        Создает объект вида деятельности:
        - Проверяет, что уровень вложенности деятельностей не превышает 3 уровня.
        - Сохраняет в базу данных
        """
        parent = None
        if parent_id:
            parent = self.repo.get_activity_by_id(db, parent_id)
            if not parent:
                raise ValueError("Not found")
            if parent.level >= self.MAX_LEVEL:
                raise ValueError("Max depth is 3")
        activity = Activity(name=name, parent=parent, level=0 if not parent else parent.level + 1)
        db.add(activity)
        db.commit()
        logger.info("Добавлен новый вид деятельности: %s", activity.name)
        db.refresh(activity)
        return activity
