import logging
from datetime import datetime
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel, constr, confloat, conint
from typing import Optional

from model_utils import load_model
from train import preprocess

logger = logging.getLogger("uvicorn.error")


class ResaleInput(BaseModel):
    town: str
    flat_type: str
    storey_range: constr(pattern=r"^\d{2}\s+TO\s+\d{2}$")
    lease_commence_date: conint(ge=1966, le=datetime.now().year)

    month: Optional[constr(pattern=r"^\d{4}-\d{2}$")] = None
    floor_area_sqm: Optional[confloat(gt=0)] = None
    flat_model: Optional[str] = None
    block: Optional[str] = None
    street_name: Optional[str] = None
    remaining_lease: Optional[constr(pattern=r"\d+\s+years?\s+\d+\s+months?")] = None

    class Config:
        json_schema_extra = {
            "example": {
                "month": "2024-05",
                "town": "ANG MO KIO",
                "flat_type": "4 ROOM",
                "block": "406",
                "street_name": "ANG MO KIO AVE 10",
                "floor_area_sqm": 92.0,
                "storey_range": "04 TO 06",
                "flat_model": "MODEL A",
                "lease_commence_date": 1980,
                "remaining_lease": "61 years 04 months",
            }
        }


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    try:
        model = load_model()
        logger.info("Loaded model from saved_model")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        # logger.info("saved model not found, training model")
        # train_and_save(csv_path="/data/csvs")
        # model = load_model()
        model = None
    yield


app = FastAPI(title="HDB Resale Price Predictor", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


def preprocess_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the *same* feature-engineering pipeline you used in training
    (age, storey_mean, remaining_lease_years, dtype casting …).
    """
    return preprocess(df)  # reuse the function from training


@app.post("/predict", response_model=dict)
async def predict_price(payload: ResaleInput):
    if model is None:
        raise HTTPException(500, "Model not loaded")

    df = pd.DataFrame([payload.model_dump()])

    # feature engineering (must match training exactly)
    try:
        df_feats = preprocess_features(df)
    except Exception as err:
        raise HTTPException(400, f"Pre-processing failed: {err}")

    # 3. run prediction in threadpool (keeps event-loop non-blocking)
    try:
        preds = await run_in_threadpool(model.predict, df_feats)
        return {"prediction": float(preds[0])}  # JSON-serialisable
    except Exception as err:
        raise HTTPException(500, f"Inference failed: {err}")
