from typing import List, Optional

from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    """Pydantic модель для возврата данных о деятельности организации"""

    name: str = Field(..., min_length=2, max_length=200)


class ActivityResponse(ActivityBase):
    """Организации по виду деятельности"""

    id: int
    level: int
    parent_id: Optional[int] = None

    model_config = {
        "from_attributes": True,
        "extra": "forbid",
        "strict": True,
    }


class ActivityTreeResponse(ActivityResponse):
    """Для древовидного вывода деятельности организаций"""

    children: List["ActivityTreeResponse"] = Field(default_factory=list)

    model_config = {
        "from_attributes": True,
    }


ActivityTreeResponse.model_rebuild()  # Для избежания forward reference ?
