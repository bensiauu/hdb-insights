from typing import Any
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Base URL for your resale-data API
BASE_URL = "http://localhost:8000/api/resale-data"

# App title
st.title("📊 HDB Resale Data Explorer")

# Filter controls
flat_models = ["All", "1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"]
selected_flat = st.selectbox("Flat Type", flat_models)
limit = st.slider("Limit", min_value=1, max_value=500, value=100)
offset = st.number_input("Offset", min_value=0, value=0)


# Cached data loader that dynamically fetches based on controls
def load_data(flat_model: str, limit: int, offset: int) -> pd.DataFrame:
    params: dict[str, Any] = {"limit": limit, "offset": offset}
    if flat_model != "All":
        params["flat_model"] = flat_model
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception as ex:
        st.error(f"Error fetching data: {ex}")
        return pd.DataFrame()


# Use caching to avoid refetching unless inputs change
@st.cache_data(show_spinner=True)
def get_data(flat: str, limit: int, offset: int):
    return load_data(flat, limit, offset)


# Fetch the data
df = get_data(selected_flat, limit, offset)

# Display results
if not df.empty:
    st.subheader(f"Showing {len(df)} records")
    st.dataframe(df)

    # 1. Time-Series Trend of Average Price
    df["month_dt"] = pd.to_datetime(df["month"], format="%Y-%m-%d")
    monthly_avg = df.groupby("month_dt")["resale_price"].mean()
    st.subheader("Average Resale Price Over Time")
    st.line_chart(monthly_avg)

    # 2. Box Plot by Flat Model
    st.subheader("Price Distribution by Flat Model")
    fig_box = px.box(
        df, x="flat_model", y="resale_price", title="Resale Price by Flat Model"
    )
    st.plotly_chart(fig_box)

    # 3. Scatter: Floor Area vs Price
    st.subheader("Floor Area vs. Resale Price")
    st.scatter_chart(df, x="floor_area_sqm", y="resale_price")

    # 4. Bar: Storey Range Counts
    st.subheader("Transactions by Storey Range")
    storey_counts = df["storey_range"].value_counts().sort_index()
    st.bar_chart(storey_counts)

    # 5. Heatmap: Town × Flat Model Prices
    st.subheader("Heatmap: Town and Flat Model Prices")
    pivot = df.pivot_table(
        index="town", columns="flat_model", values="resale_price", aggfunc="mean"
    )
    st.dataframe(pivot.style.background_gradient(cmap="viridis"))
else:
    st.warning("No data returned from the API.")
