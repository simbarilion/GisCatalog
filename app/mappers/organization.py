from geoalchemy2.shape import to_shape
from sqlalchemy import Sequence

from app.db.models import Organization


def map_organization(org: Organization):
    """
    Преобразует geometry данные в координаты (lon, lat).
    Преобразует объект Organization в словарь значений
    """
    building = org.building
    lon, lat = to_shape(building.location).coords[0]

    return {
        "id": org.id,
        "name": org.name,
        "building": {
            "id": building.id,
            "address": building.address,
            "latitude": lat,
            "longitude": lon,
        },
        "phones": [{"id": p.id, "phone": p.phone} for p in org.phones],
        "activities": [
            {
                "id": a.id,
                "name": a.name,
                "level": a.level,
                "parent_id": a.parent_id,
            }
            for a in org.activities
        ],
    }


def map_orgs_list(orgs: Sequence[Organization]) -> list[dict]:
    """Преобразует коллекцию объектов Organization в список словарей значений"""
    return [
        {
            "id": org.id,
            "name": org.name,
            "latitude": lat,
            "longitude": lon,
        }
        for org, lat, lon in orgs
    ]
