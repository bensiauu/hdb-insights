"""
Train an HDB resale-price model with LightGBM using an enriched feature set.

Run:
    python backend/model-service/train.py data/raw_csvs/
"""

from __future__ import annotations
import re
import sys
import os
from pathlib import Path
from typing import List

import joblib
import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ──────────────────── config ────────────────────
MODEL_PATH = Path("saved_model.pkl")
RANDOM_STATE = 4

NUM_FEATS: List[str] = [
    "floor_area_sqm",
    "age",
    "storey_mean",
    "remaining_lease_years",
    "resale_year",
    "resale_month",
]

CAT_FEATS: List[str] = [
    "town",
    "flat_type",
    "flat_model",
    "block",
    "street_name",
]

TARGET = "resale_price"


# ──────────────────── helpers ────────────────────
def load_concat_csvs(csv_dir: Path) -> pd.DataFrame:
    """Read every *.csv beneath `csv_dir`."""
    frames = []
    for root, _, files in os.walk(csv_dir):
        for fname in files:
            if fname.lower().endswith(".csv"):
                frames.append(pd.read_csv(Path(root) / fname))
    if not frames:
        raise FileNotFoundError(f"No CSV files under {csv_dir}")
    return pd.concat(frames, ignore_index=True)


_storey_pat = re.compile(r"(\d+)\s+TO\s+(\d+)")
_rl_pat = re.compile(r"(\d+)\s+years?\s+(\d+)\s+months?")


def parse_storey_mean(val):
    """Convert '04 TO 06' → 5.0; keep NaNs safe."""
    if pd.isna(val):
        return np.nan
    if not isinstance(val, str):
        return float(val)
    m = _storey_pat.fullmatch(val.strip())
    return (int(m.group(1)) + int(m.group(2))) / 2 if m else np.nan


def parse_remaining_lease(val):
    """Convert '61 years 04 months' → 61.33; handle NaNs / numeric."""
    if pd.isna(val):
        return np.nan
    if not isinstance(val, str):
        return float(val)  # already numeric or int
    m = _rl_pat.fullmatch(val.strip())
    return int(m.group(1)) + int(m.group(2)) / 12 if m else np.nan


FLOOR_AREA_MEDIAN = 93.0
UNKNOWN_STR = "UNKNOWN"
TODAY = pd.Timestamp.today()


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ── fill optional fields ──
    df["month"].fillna(TODAY.strftime("%Y-%m"), inplace=True)
    df["floor_area_sqm"].fillna(FLOOR_AREA_MEDIAN, inplace=True)
    df["flat_model"].fillna(UNKNOWN_STR, inplace=True)
    df["block"].fillna(UNKNOWN_STR, inplace=True)
    df["street_name"].fillna(UNKNOWN_STR, inplace=True)

    # ── convert dates ──
    df["lease_commence_date"] = pd.to_datetime(
        df["lease_commence_date"], errors="coerce"
    )
    df["month"] = pd.to_datetime(df["month"], format="%Y-%m", errors="coerce")

    # ── engineered features ──
    df["age"] = TODAY.year - df["lease_commence_date"].dt.year
    df["resale_year"] = df["month"].dt.year
    df["resale_month"] = df["month"].dt.month
    df["storey_mean"] = df["storey_range"].apply(parse_storey_mean)

    # remaining_lease_years: use parsed value **or** 99 − age
    parsed_rl = df["remaining_lease"].apply(parse_remaining_lease)
    df["remaining_lease_years"] = np.where(
        parsed_rl.notna(),
        parsed_rl,
        np.clip(99 - df["age"], a_min=0, a_max=None),  # never negative
    )

    # ── categoricals ──
    for col in CAT_FEATS:
        df[col] = df[col].astype("category")

    # ── drop raw text/date cols ──
    df = df.drop(
        columns=[
            c
            for c in [
                "month",
                "storey_range",
                "lease_commence_date",
                "remaining_lease",
                "resale_price",  # ignored if absent during inference
            ]
            if c in df.columns
        ]
    )

    # return model-ready order
    return df[NUM_FEATS + CAT_FEATS]


# ──────────────────── training ────────────────────
def train_and_save(csv_dir: Path) -> None:
    raw_df = load_concat_csvs(csv_dir)
    df = preprocess(raw_df)

    y = raw_df[TARGET]
    X = df[NUM_FEATS + CAT_FEATS]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_STATE
    )

    model = lgb.LGBMRegressor(
        n_estimators=3000,
        learning_rate=0.03,
        num_leaves=63,
        min_data_in_leaf=50,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        random_state=RANDOM_STATE,
    )

    model.fit(
        X_train,
        y_train,
        eval_set=[(X_val, y_val)],
        eval_metric="l1",  # MAE
        callbacks=[
            lgb.early_stopping(stopping_rounds=100, verbose=True),
            lgb.log_evaluation(period=50),
        ],
        categorical_feature=CAT_FEATS,
    )

    preds = model.predict(X_val, num_iteration=model.best_iteration_)
    print(f"MAE : {mean_absolute_error(y_val, preds):.2f}")
    print(f"MSE : {mean_squared_error(y_val, preds):.2f}")
    print(f"R²  : {r2_score(y_val, preds):.4f}")
    print(f"Best iteration: {model.best_iteration_}")

    joblib.dump(model, MODEL_PATH, compress=3)
    print(f"Model saved → {MODEL_PATH.resolve()}")


def load_model(path: Path = MODEL_PATH) -> lgb.LGBMRegressor:
    return joblib.load(path)


# ──────────────────── CLI ────────────────────
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: train_lightgbm.py /path/to/csv_dir")
    train_and_save(Path(sys.argv[1]).expanduser().resolve())
