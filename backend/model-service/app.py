import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from model_utils import load_model, preprocess_data, train_and_save

logger = logging.getLogger("uvicorn.error")


class ResaleInput(BaseModel):
    town: str = Field(..., examples=["Town"])
    flat_model: str = Field(..., examples=["Improved"])
    floor_area_sqm: float = Field(..., examples=[75.0])
    storey_range: str = Field(..., examples=["01 TO 03"])
    remaining_lease: float = Field(..., examples=[75.0])
    flat_type: str = Field(..., examples=["3 ROOM"])




@asynccontextmanager
async def lifespan(app:FastAPI):
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
        raise RuntimeError("failed to load model")
    yield


app = FastAPI(title="HDB Resale Price Predictor", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"],
                   allow_headers=["*"])


@app.post("/predict")
async def predict_price(payload: ResaleInput):
    try:
        df = pd.DataFrame([payload])
        df_features = preprocess_data(df)
        preds = model.predict(df_features)
        return {"prediction": preds[0]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
