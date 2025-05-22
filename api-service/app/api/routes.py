from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.repositories.resale import get_all_resale_records
from app.schemas.schemas import ResaleRecordResponse


router = APIRouter()

@router.get("/resale-data", response_model=List[ResaleRecordResponse])
def get_resale_data(db: Session = Depends(get_db),
flat_type: Optional[str] = Query(None), limit: int = Query(100, ge=1, le=500), offset: int = Query(0, ge=0)):
    return get_all_resale_records(db)
