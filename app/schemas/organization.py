from typing import List, Optional

from pydantic import BaseModel, Field

from .activity import ActivityResponse
from .building import BuildingResponse
from .phone import PhoneResponse


class OrganizationBase(BaseModel):
    """Pydantic модель для возврата данных об организациях"""

    name: str = Field(..., min_length=2, max_length=255, description="Название организации")


class OrganizationResponse(OrganizationBase):
    """Полная карточка организации"""

    id: int
    building: BuildingResponse
    phones: List[PhoneResponse] = Field(default_factory=list)
    activities: List[ActivityResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
        "extra": "forbid",
        "strict": True,
        "validate_assignment": True,
    }


class OrganizationListResponse(BaseModel):
    """Список организаций с пагинацией и фильтрами"""

    items: List[OrganizationResponse]
    total: int
    page: Optional[int] = None
    size: Optional[int] = None

    model_config = {
        "from_attributes": True,
    }


class OrganizationSearchByName(BaseModel):
    """Организация по названию"""

    name: str = Field(..., min_length=2, max_length=255)


class OrganizationsByBuilding(BaseModel):
    """Организации в конкретном здании"""

    building_id: int


class OrganizationsByActivity(BaseModel):
    """Организации по виду деятельности: с учётом вложенности"""

    activity_id: int
    include_children: bool = Field(True, description="Включать дочерние виды деятельности")


class OrganizationsInRadius(BaseModel):
    """Организации в радиусе от точки"""

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_meters: float = Field(..., gt=0, le=50000, description="Радиус в метрах (максимум 50 км)")


class OrganizationsInBBox(BaseModel):
    """Организации в прямоугольной области: Bounding Box"""

    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
