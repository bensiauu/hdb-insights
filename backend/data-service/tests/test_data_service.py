import os
from datetime import date

from fastapi.testclient import TestClient

from app.db.database import Base, SessionLocal, engine
from app.main import app
from app.models.models import ResaleRecord

db_path = "test.db"

if os.path.exists(db_path):
    os.remove(db_path)

os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"


# create tables
Base.metadata.create_all(bind=engine)

# insert sample data
with SessionLocal() as db:
    db.add_all(
        [
            ResaleRecord(
                town="ANG MO KIO",
                month=date(2020, 1, 1),
                flat_type="3 ROOM",
                block="101",
                street_name="AMK AVE 1",
                storey_range="04 TO 06",
                floor_area_sqm=65.0,
                flat_model="MODEL A",
                lease_commence_date=1980,
                resale_price=400000,
            ),
            ResaleRecord(
                town="BEDOK",
                month=date(2019, 6, 1),
                flat_type="4 ROOM",
                block="202",
                street_name="BEDOK NORTH",
                storey_range="07 TO 09",
                floor_area_sqm=90.0,
                flat_model="MODEL B",
                lease_commence_date=1995,
                resale_price=500000,
            ),
        ]
    )
    db.commit()

client = TestClient(app)


def test_get_history_filter_by_town():
    resp = client.get("/api/history", params={"town": "ANG MO KIO"})
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["town"] == "ANG MO KIO"


def test_get_options():
    resp = client.get("/api/options/town")
    assert resp.status_code == 200
    towns = resp.json()
    assert set(towns) == {"ANG MO KIO", "BEDOK"}

    resp = client.get("/api/options/flat_type")
    assert resp.status_code == 200
    flats = resp.json()
    assert set(flats) == {"3 ROOM", "4 ROOM"}

    resp = client.get("/api/options/storey_range")
    assert resp.status_code == 200
    storey = resp.json()
    assert set(storey) == {"04 TO 06", "07 TO 09"}
