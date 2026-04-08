from pydantic import BaseModel, Field


class ActivityBase(BaseModel):
    """Pydantic модель для возврата данных о деятельности организации"""

    name: str = Field(..., min_length=2, max_length=200)
