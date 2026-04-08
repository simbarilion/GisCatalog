from typing import List

from pydantic import BaseModel, Field


class BuildingBase(BaseModel):
    """Pydantic модель для возврата данных о зданиях"""

    address: str = Field(..., min_length=5, max_length=500, description="Полный адрес здания")
    latitude: float = Field(..., ge=-90, le=90, description="Широта")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота")


class BuildingResponse(BuildingBase):
    """Полная информация о здании"""

    id: int

    model_config = {
        "from_attributes": True,
        "extra": "forbid",
        "strict": True,
    }


class BuildingListResponse(BaseModel):
    """Список зданий"""

    items: List[BuildingResponse]
    total: int

    model_config = {
        "from_attributes": True,
    }
