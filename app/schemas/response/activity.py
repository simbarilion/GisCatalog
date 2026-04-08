from typing import List, Optional

from pydantic import Field

from app.schemas.common import ActivityBase


class ActivityResponse(ActivityBase):
    """Организации по виду деятельности"""

    id: int
    level: int
    parent_id: Optional[int] = None
    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }


class ActivityTreeResponse(ActivityResponse):
    """Для древовидного вывода деятельности организаций"""

    children: List["ActivityTreeResponse"] = Field(default_factory=list)
    model_config = {
        "from_attributes": True,
    }


ActivityTreeResponse.model_rebuild()  # нужен для self-reference
