import os

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (make_scorer, mean_absolute_error,
                             mean_squared_error, r2_score)
from sklearn.model_selection import (RandomizedSearchCV, StratifiedKFold,
                                     train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

CSV_DIR = "../api-service/ResaleFlatPrices/"
dfs = []
for root, dirs, files in os.walk(CSV_DIR):
    for file in files:
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(root, file))
            dfs.append(df)

df = pd.concat(dfs, ignore_index=True)


# Preprocessing and feature engineering
def preprocess_data(df):
    df["lease_commence_date"] = pd.to_datetime(df["lease_commence_date"])
    df["age"] = pd.to_datetime("today").year - df["lease_commence_date"].dt.year
    return df


df = preprocess_data(df)

# Define features and target
features = ["town", "flat_type", "storey_range", "floor_area_sqm", "flat_model", "age"]

X = df[features]
Y = df["resale_price"]

# Split data
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=4)

# Create preprocessing pipelines
numeric_features = ["floor_area_sqm", "age"]
categorical_features = ["town", "flat_type", "flat_model", "storey_range"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(), categorical_features),
    ]
)

pipeline = Pipeline(
    [("preprocessor", preprocessor), ("model", RandomForestRegressor(random_state=4))]
)

# Define hyperparameter search space
param_distributions = {
    "model__n_estimators": [100, 200, 300, 400, 500],
    "model__max_depth": [None, 10, 20, 30, 40],
    "model__min_samples_split": [2, 5, 10],
    "model__min_samples_leaf": [1, 2, 5],
    "model__max_features": ["sqrt", "log2"],
}

# Set up RandomizedSearchCV
random_search = RandomizedSearchCV(
    estimator=pipeline,
    param_distributions=param_distributions,
    n_iter=50,  # Increase iterations
    cv=5,  # Use proper cross-validation
    n_jobs=-1,
    verbose=2,
    scoring="neg_mean_absolute_error",
    random_state=4,
)

# Fit model
random_search.fit(X_train, Y_train)

# Model evaluation
Y_pred = random_search.predict(X_test)
mae = mean_absolute_error(Y_test, Y_pred)
mse = mean_squared_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

# Output results
print(f"Best parameters: {random_search.best_params_}")
print(f"Mean Absolute Error: {mae}")
print(f"Mean Squared Error: {mse}")
print(f"R² score: {r2}")

# save model
joblib.dump(random_search.best_estimator_, "resale_predictor.pkl")
