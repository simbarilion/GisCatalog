import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from app.api.routes.health import health_router
from app.api.routes.organizations import organizations_router

load_dotenv()
app = FastAPI(
    title="Gis Catalog API",
    description="Справочник организаций, зданий и видов деятельности. "
    "Авторизация: все запросы требуют статический API ключ в заголовке `API-Key`.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Получение организаций",
            "description": "Операции со справочником организаций: поиск, фильтрация, геопоиск. "
            "Все запросы требуют наличия статического API-ключа в заголовке `API-Key`",
        },
        {"name": "Health", "description": "Проверка работоспособности API, соединения с базой данных"},
    ],
    contact={
        "name": "Popova Nadezhda",
        "email": "nadezhdapopova13@yandex.ru",
    },
)

app.include_router(organizations_router)
app.include_router(health_router)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=404, content={"detail": str(exc) or "Resource not found"})


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Server error"})


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENV", "development").lower() == "development",
    )
