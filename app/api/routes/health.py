from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

health_router = APIRouter(prefix="/health", tags=["Health checks"])


@health_router.get(
    "/",
    summary="Простая проверка работоспособности API",
    description="Возвращает статус API",
    status_code=status.HTTP_200_OK,
)
def health():
    """Проверка, что API запущено"""
    return {"status": "ok"}


@health_router.get(
    "/db",
    summary="Проверка подключения к базе данных",
    description="Выполняет простой запрос к PostgreSQL для проверки соединения",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def db_health(db: Session = Depends(get_db)):
    """Проверка соединения с базой"""
    try:
        db.execute(text("SELECT 1")).scalar_one()
        return {"status": "ok", "database": "connected", "message": "Successfully connected to PostgreSQL + PostGIS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
