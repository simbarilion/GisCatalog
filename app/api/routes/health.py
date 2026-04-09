from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.api.dependencies.common import DBSession

health_router = APIRouter(prefix="/health", tags=["Health checks"])


@health_router.get("/")
def health():
    """Проверка, что API запущено"""
    return {"status": "ok"}


@health_router.get("/db")
def db_health(db: DBSession):
    """Проверка соединения с базой"""
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="Database unavailable")
