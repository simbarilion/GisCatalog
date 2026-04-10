from pydantic import BaseModel, Field, model_validator


class OrganizationSearchByName(BaseModel):
    """Организация по названию"""

    name: str = Field(..., min_length=2, max_length=255)


class OrganizationsByBuilding(BaseModel):
    """Организации в конкретном здании"""

    building_id: int


class OrganizationsByActivity(BaseModel):
    """Организации по виду деятельности: с учётом вложенности"""

    activity_id: int


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

    @model_validator(mode="after")
    def validate_bbox(self):
        if self.min_lat >= self.max_lat:
            raise ValueError("Минимальная широта не должна быть больше максимальной широты")
        if self.min_lon >= self.max_lon:
            raise ValueError("Минимальная долгота не должна быть больше максимальной долготы")
        return self
