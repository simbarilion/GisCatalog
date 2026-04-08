from pydantic import BaseModel, Field


class PhoneResponse(BaseModel):
    """Pydantic модель для возврата данных о телефоне организации"""

    id: int
    phone: str = Field(..., min_length=5, max_length=20)

    model_config = {
        "from_attributes": True,
        "extra": "forbid",
    }
