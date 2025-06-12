from pydantic import BaseModel
from datetime import date


class ResaleRecordResponse(BaseModel):
    month: date
    town: str
    block: str
    street_name: str
    storey_range: str
    floor_area_sqm: float
    flat_model: str
    lease_commence_date: int
    resale_price: int
    flat_type: str

    class Config:
        from_attributes = True
