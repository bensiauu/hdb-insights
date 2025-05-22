import pathlib
import pandas as pd
import os
from datetime import datetime

from sqlalchemy import create_engine


CSV_PATH = pathlib.Path("../ResaleFlatPrices/")
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/hdb_resale"

expected_cols = [
    "month", "town", "flat_type", "block", "street_name",
    "storey_range", "floor_area_sqm", "flat_model",
    "lease_commence_date", "resale_price"
]

# collect and normalize data from all CSVs
dataframes = []

for csv_file in sorted(CSV_PATH.glob("*.csv")):
    print(f"Processing {csv_file.name}")
    df = pd.read_csv(csv_file)

    df['month'] = pd.to_datetime(df['month'], format="%Y-%m")
    df['block'] = df['block'].astype(str)
    df['floor_area_sqm'] = df['floor_area_sqm'].astype(float)
    df['resale_price'] = df['resale_price'].astype(int)
    df['lease_commence_date'] = df['lease_commence_date'].astype(int)

    df = df[expected_cols]
    dataframes.append(df)

combined_df = pd.concat(dataframes, ignore_index=True)
engine = create_engine(DATABASE_URL)
combined_df.to_sql("resale_prices",engine,if_exists="append", index=False)
