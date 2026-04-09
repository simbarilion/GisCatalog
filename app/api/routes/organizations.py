from fastapi import APIRouter
from fastapi.params import Depends

from app.api.dependencies.auth import get_api_key
from app.api.dependencies.common import (
    Activity_id,
    Building_id,
    DBSession,
    Include_children,
    Lat,
    Limit,
    Lon,
    Name,
    Offset,
    Org_id,
    Radius_m,
)
from app.schemas.request import OrganizationsInBBox
from app.schemas.response import OrganizationListResponse, OrganizationResponse
from app.services.organization import OrganizationService

organizations_router = APIRouter(prefix="/orgs", tags=["Получение организаций"], dependencies=[Depends(get_api_key)])

service = OrganizationService()


@organizations_router.get("/by_id", response_model=OrganizationResponse)
def get_organization_by_id(db: DBSession, org_id: Org_id):
    """Возвращает полную информацию об организации"""
    return service.get_organization_by_id(db=db, org_id=org_id)


@organizations_router.get("/by_name", response_model=OrganizationListResponse)
def get_by_name(db: DBSession, name: Name, limit: Limit = 50, offset: Offset = 0):
    """Возвращает список организаций по наименованию"""
    return service.get_by_name(db=db, name=name, limit=limit, offset=offset)


@organizations_router.get("/by_building", response_model=OrganizationListResponse)
def get_by_building(db: DBSession, building_id: Building_id, limit: Limit = 50, offset: Offset = 0):
    """Возвращает список организаций в здании"""
    return service.get_by_building(db=db, building_id=building_id, limit=limit, offset=offset)


@organizations_router.get("/by_activity", response_model=OrganizationListResponse)
def get_by_activity(
    db: DBSession,
    activity_id: Activity_id,
    include_children: Include_children = True,
    limit: Limit = 50,
    offset: Offset = 0,
):
    """Возвращает список организаций с вложенностью по виду деятельности"""
    return service.get_by_activity(
        db=db, activity_id=activity_id, include_children=include_children, limit=limit, offset=offset
    )


@organizations_router.get("/in_radius", response_model=OrganizationListResponse)
def get_in_radius(db: DBSession, lat: Lat, lon: Lon, radius_m: Radius_m, limit: Limit = 50, offset: Offset = 0):
    """Возвращает список организаций в заданном радиусе на карте"""
    return service.get_in_radius(db=db, lat=lat, lon=lon, radius_m=radius_m, limit=limit, offset=offset)


@organizations_router.get("/in_bbox", response_model=OrganizationListResponse)
def get_in_bbox(db: DBSession, params: OrganizationsInBBox = Depends(), limit: Limit = 50, offset: Offset = 0):
    """Возвращает список организаций в заданной прямоугольной области на карте"""
    return service.get_in_bbox(
        db=db,
        min_lat=params.min_lat,
        max_lat=params.max_lat,
        min_lon=params.min_lon,
        max_lon=params.max_lon,
        limit=limit,
        offset=offset,
    )
