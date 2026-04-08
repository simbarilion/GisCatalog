from typing import List

from pydantic import BaseModel, Field

from app.schemas.common import OrganizationBase

from .activity import ActivityResponse
from .building import BuildingResponse
from .phone import PhoneResponse


class OrganizationResponse(OrganizationBase):
    """Полная карточка организации"""

    id: int
    building: BuildingResponse
    phones: List[PhoneResponse] = Field(default_factory=list)
    activities: List[ActivityResponse] = Field(default_factory=list)
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }


class OrganizationShortResponse(BaseModel):
    """Краткая карточка организации"""

    id: int
    name: str
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }


class OrganizationListResponse(BaseModel):
    """Список организаций с пагинацией и фильтрами"""

    items: List[OrganizationShortResponse]
    total: int
    page: int
    size: int
    model_config = {
        "from_attributes": True,
    }
