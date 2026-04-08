from pydantic import BaseModel, Field


class OrganizationBase(BaseModel):
    """Pydantic модель для возврата данных об организациях"""

    name: str = Field(..., min_length=2, max_length=255, description="Название организации")
