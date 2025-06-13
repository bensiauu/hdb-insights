from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import distinct

from app.db.database import get_db
from app.models.models import ResaleRecord


def get_all_resale_records(
    db: Session = Depends(get_db),
    limit=100,
    town: Optional[str] = None,
    offset: int = 0,
    flat_type: Optional[str] = None,
) -> List[ResaleRecord]:
    query = db.query(ResaleRecord)
    if town:
        query = query.filter(ResaleRecord.town == town)
    if flat_type:
        query = query.filter(ResaleRecord.flat_type == flat_type)

    return (
        query.order_by(ResaleRecord.lease_commence_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_all_towns(db: Session = Depends(get_db)):
    """
    Returns distinct towns in DB
    """

    results = db.query(distinct(ResaleRecord.town)).order_by(ResaleRecord.town).all()
    return [row[0] for row in results]


def get_all_flat_types(db: Session = Depends(get_db)):
    """
    Returns distinct flat types in DB
    """
    results = (
        db.query(distinct(ResaleRecord.flat_type))
        .order_by(ResaleRecord.flat_type)
        .all()
    )
    return [row[0] for row in results]
