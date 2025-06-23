import importlib.util

from fastapi.testclient import TestClient

import model_utils

model_path = "app.py"
spec = importlib.util.spec_from_file_location("model_app", model_path)
model_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_app)


model_utils.MODEL_PATH = "saved_model.pkl"

sample_payload = {
    "town": "ANG MO KIO",
    "flat_type": "4 ROOM",
    "storey_range": "04 TO 06",
    "lease_commence_date": 1990,
    "floor_area_sqm": 90.0,
    "flat_model": "MODEL A",
    "month": "2024-01",
}


def test_predict_endpoint():
    with TestClient(model_app.app) as client:
        resp = client.post("/predict", json=sample_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert "prediction" in data
        assert isinstance(data["prediction"], float)
