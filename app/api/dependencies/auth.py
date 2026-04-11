import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.logging import setup_logger

load_dotenv()

logger = setup_logger(__name__, level="INFO")

API_KEY_NAME = "API-Key"
API_KEY = os.getenv("SECRET_API_KEY")

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        logger.info("API-Key успешно подключен")
        return api_key
    logger.error("Неверный или отсутствующий Api Key")
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Неверный или отсутствующий Api Key",
        headers={"WWW-Authenticate": "ApiKey"},
    )
