from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.resale import (
    get_all_resale_records,
    get_all_towns,
    get_all_flat_types,
    get_all_storey,
)
from app.schemas.schemas import ResaleRecordResponse


router = APIRouter()
opts_router = APIRouter()


@router.get("/history", response_model=List[ResaleRecordResponse])
def get_resale_data(
    db: Session = Depends(get_db),
    flat_type: Optional[str] = Query(None),
    town: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    return get_all_resale_records(
        db, limit=limit, offset=offset, flat_type=flat_type, town=town
    )


@opts_router.get("/town", response_model=List[str])
def get_available_towns(db: Session = Depends(get_db)):
    return get_all_towns(db)


@opts_router.get("/flat_type", response_model=List[str])
def get_available_flat_types(db: Session = Depends(get_db)):
    return get_all_flat_types(db)


@opts_router.get("/storey_range", response_model=List[str])
def get_available_storey(db: Session = Depends(get_db)):
    return get_all_storey(db)
