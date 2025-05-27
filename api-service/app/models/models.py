from sqlalchemy import Column, Date, Float, Integer, String

from app.db.database import Base


class ResaleRecord(Base):
    __tablename__ = "resale_prices"
    id = Column(Integer, primary_key=True, index=True)
    town = Column(String)
    month = Column(Date, nullable=False)
    flat_type = Column(String)
    block = Column(String)
    street_name = Column(String)
    storey_range = Column(String)
    floor_area_sqm = Column(Float)
    flat_model = Column(String)
    lease_commence_date = Column(Integer)
    resale_price = Column(Integer)
