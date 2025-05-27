from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.models import ResaleRecord


def get_all_resale_records(db: Session = Depends(get_db), limit=100, town: Optional[str] = None, offset: int = 0, flat_type: Optional[str]=None) -> List[ResaleRecord]:
    query = db.query(ResaleRecord)
    if town:
        query = query.filter(ResaleRecord.town == town)
    if flat_type:
        query = query.filter(ResaleRecord.flat_type == flat_type)

    return query.order_by(ResaleRecord.month.desc()).offset(offset).limit(limit).all()
