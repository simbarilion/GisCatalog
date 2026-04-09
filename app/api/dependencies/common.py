from fastapi import Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated

from app.db.session import get_db

DBSession = Annotated[Session, Depends(get_db)]

Limit = Annotated[int, Query(le=500)]
Offset = Annotated[int, Query()]

Org_id = Annotated[int, Query(..., ge=0)]
Name = Annotated[str, Query(...)]
Building_id = Annotated[int, Query(..., ge=0)]
Activity_id = Annotated[int, Query(..., ge=0)]
Include_children = Annotated[bool, Query(default=True)]
Lat = Annotated[float, Query(..., ge=-90.0, le=90.0)]
Lon = Annotated[float, Query(..., ge=-180.0, le=180.0)]
Radius_m = Annotated[float, Query(..., ge=0.0, le=50000)]
