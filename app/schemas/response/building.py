from typing import List

from pydantic import BaseModel

from app.schemas.common import BuildingBase


class BuildingResponse(BuildingBase):
    """Полная информация о здании"""

    id: int
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }


class BuildingListResponse(BaseModel):
    """Список зданий"""

    items: List[BuildingResponse]
    total: int
    model_config = {
        "from_attributes": True,
    }
