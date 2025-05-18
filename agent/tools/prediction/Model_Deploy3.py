#!/usr/bin/env python3
"""
Model Deployment Script:
 - Loads the saved XGBoost model, target encoder, and town aggregated statistics.
 - Accepts an input (dictionary or DataFrame) that may contain a subset of the table columns.
 - Handles missing categorical values by filling them with "unknown".
 - Preprocesses the input (date conversion, time-based features, storey_range conversion, lease conversion).
 - Fills in extended town aggregated features (town_mean, town_median, town_std, town_count) from saved statistics.
 - Prepares the final features and applies target encoding.
 - Casts all features to numeric types so that XGBoost does not complain.
 - Predicts the house price.
 - Computes SHAP values to explain which input features contributed to the prediction.
 - Prints final features and processed input (all columns) and outputs the SHAP explanation.
"""

import pandas as pd
import numpy as np
import joblib
import category_encoders as ce
from xgboost import XGBRegressor
import shap

# Configure pandas to display all columns when printing.
pd.set_option('display.max_columns', None)


def load_artifacts():
    """
    Load and return the saved XGBoost model, target encoder, and town aggregated statistics.
    Assumes files "xgboost_house_price_model.joblib", "target_encoder.joblib", and optionally "town_stats.joblib" exist.
    """
    # model = joblib.load("xgboost_house_price_model.joblib")
    # encoder = joblib.load("target_encoder.joblib")
    model = joblib.load("./agent/tools/prediction/xgboost_house_price_model.joblib")
    encoder = joblib.load("./agent/tools/prediction/target_encoder.joblib")
    try:
        # town_stats = joblib.load("town_stats.joblib")
        town_stats = joblib.load("./agent/tools/prediction/town_stats.joblib")
    except Exception:
        town_stats = {}
    return model, encoder, town_stats


def convert_storey_range(s):
    """
    Convert a storey_range string (e.g., "04 to 06") to a numeric value (midpoint).
    """
    try:
        lower, upper = s.split(" to ")
        return (int(lower) + int(upper)) / 2
    except Exception:
        return np.nan


def convert_remaining_lease(s):
    """
    Convert a remaining_lease string (e.g., "60 years 08 months") to a numeric value in years.
    """
    try:
        parts = s.split()
        years = int(parts[0])
        months = int(parts[2])
        return years + months / 12.0
    except Exception:
        return np.nan


def preprocess_input(df):
    """
    Preprocess the input DataFrame:
      - Ensure required columns exist (if missing, add defaults).
      - Fill missing values for expected columns.
      - Convert 'month' (format "YYYY-MM") to datetime.
      - Create time-based features: 'year', 'month_sin', 'month_cos'.
      - Convert 'storey_range' into 'storey_range_numeric'.
      - Convert lease-related columns to numeric.
    """
    expected_defaults = {
        "month": np.nan,  # Expected as a string "YYYY-MM"
        "storey_range": np.nan,  # e.g., "04 to 06"
        "town": "unknown",
        "flat_type": "unknown",
        "flat_model": "unknown",
        "street_name": "unknown",  # New feature for fine-grained location.
        "floor_area_sqm": np.nan,
        "lease_commence_date": np.nan,
        "remaining_lease": np.nan
    }
    for col, default in expected_defaults.items():
        if col not in df.columns:
            df[col] = default
        else:
            df[col] = df[col].fillna(default)

    # Convert 'month' to datetime.
    if df['month'].notna().any():
        df['month'] = pd.to_datetime(df['month'], format='%Y-%m', errors='coerce')
    else:
        df['month'] = pd.NaT

    # Create time-based features.
    df['year'] = df['month'].dt.year
    df['month_num'] = df['month'].dt.month
    df['month_sin'] = df['month_num'].apply(lambda m: np.sin(2 * np.pi * m / 12) if pd.notnull(m) else np.nan)
    df['month_cos'] = df['month_num'].apply(lambda m: np.cos(2 * np.pi * m / 12) if pd.notnull(m) else np.nan)
    df.drop(columns=['month_num'], inplace=True)

    # Convert 'storey_range' to numeric.
    df['storey_range_numeric'] = df['storey_range'].apply(
        lambda x: convert_storey_range(x) if pd.notnull(x) else np.nan)

    # Convert lease_commence_date to numeric.
    df['lease_commence_date'] = pd.to_numeric(df['lease_commence_date'], errors='coerce')

    # Convert remaining_lease from string to numeric (years).
    df['remaining_lease'] = df['remaining_lease'].apply(
        lambda x: convert_remaining_lease(x) if isinstance(x, str) else x)

    return df


def fill_town_aggregates(df, town_stats):
    """
    Given a DataFrame df and a dictionary of town aggregated statistics (town_stats),
    fill in the extended town features: 'town_mean', 'town_median', 'town_std', 'town_count'.
    """

    def get_stats(town):
        # Convert town to uppercase for lookup.
        key = str(town).upper()
        stats = town_stats.get(key, None)
        if stats is None:
            return pd.Series([np.nan, np.nan, np.nan, np.nan],
                             index=['town_mean', 'town_median', 'town_std', 'town_count'])
        else:
            # Expect stats to be a dictionary with these keys.
            return pd.Series([
                stats.get("town_mean", np.nan),
                stats.get("town_median", np.nan),
                stats.get("town_std", np.nan),
                stats.get("town_count", np.nan)
            ], index=['town_mean', 'town_median', 'town_std', 'town_count'])

    # For each row, fill in the extended town features.
    if 'town' in df.columns:
        stats_df = df['town'].apply(lambda x: get_stats(x if pd.notnull(x) else "unknown"))
        df = pd.concat([df, stats_df], axis=1)
    else:
        df['town_mean'] = np.nan
        df['town_median'] = np.nan
        df['town_std'] = np.nan
        df['town_count'] = np.nan
    return df


def prepare_features(df, town_stats):
    """
    Prepare the final feature set required for the model.
    Expected features (based on training):
      - Categorical (target encoded later): 'town', 'flat_type', 'flat_model', 'street_name'
      - Extended town features: 'town_mean', 'town_median', 'town_std', 'town_count'
      - Numeric: 'storey_range_numeric', 'floor_area_sqm', 'lease_commence_date', 'remaining_lease'
      - Time-based: 'year', 'month_sin', 'month_cos'
    """
    # Fill extended town aggregates if not present.
    df = fill_town_aggregates(df, town_stats)

    required_features = [
        'town', 'flat_type', 'flat_model', 'street_name',
        'town_mean', 'town_median', 'town_std', 'town_count',
        'storey_range_numeric', 'floor_area_sqm', 'lease_commence_date', 'remaining_lease',
        'year', 'month_sin', 'month_cos'
    ]
    for col in required_features:
        if col not in df.columns:
            df[col] = np.nan
    return df[required_features]


def predict_house_price(input_data):
    """
    Predict the house price based on the input data.
    Accepts a dictionary or DataFrame (with any subset of columns).

    Returns:
      A tuple (predicted_price, X_input, processed_input), where:
       - predicted_price: NumPy array of predictions.
       - X_input: Final feature set (after encoding) used for prediction.
       - processed_input: Full processed DataFrame after preprocessing.
    """
    # Convert input to a DataFrame.
    if isinstance(input_data, dict):
        df_input = pd.DataFrame([input_data])
    elif isinstance(input_data, pd.DataFrame):
        df_input = input_data.copy()
    else:
        raise ValueError("Input data must be a dictionary or a DataFrame.")

    # Preprocess the input.
    processed_input = preprocess_input(df_input)

    # Load town aggregated statistics if used
    _, _, town_stats = load_artifacts()

    # Prepare the final features (this will fill extended town features if defined).
    X_input = prepare_features(processed_input, town_stats)

    # To avoid SettingWithCopyWarning, work on an explicit copy.
    X_input = X_input.copy()
    # Use all four categorical columns that were used during training.
    categorical_cols = ['town', 'flat_type', 'flat_model', 'street_name']

    # Fill missing values for categorical columns.
    for col in categorical_cols:
        X_input.loc[:, col] = X_input[col].fillna("unknown")

    # Load the saved model and target encoder.
    model, encoder, _ = load_artifacts()

    # Apply the target encoder to the categorical columns. This expects the same dimensions as it was fit with.
    X_input.loc[:, categorical_cols] = encoder.transform(X_input[categorical_cols]).astype(float)

    # Ensure that all features are numeric.
    X_input = X_input.astype(float)

    # Predict the house price.
    predicted_price = model.predict(X_input)

    return predicted_price, X_input, processed_input


def compute_shap_explanation(model, X_input):
    """
    Compute SHAP values for the input X_input and return a DataFrame listing each feature's contribution.
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_input)
    # For a single instance, shap_values has shape (num_features,). Create a DataFrame.
    shap_df = pd.DataFrame({
        'Feature': X_input.columns,
        'SHAP Value': shap_values[0]
    })
    return shap_df


# ------------------------------
# Main Execution
# ------------------------------
if __name__ == "__main__":
    # Example input: Here we simulate an input record.
    sample_input = {
        "month": "2025-01",  # Transaction month
        "storey_range": "04 to 06",  # Original floor range
        "town": "YISHUN",  # Town (provided here; if missing, will be replaced with "unknown")
        "flat_type": "4-room",
        "flat_model": "Simplified",
        "street_name": "ANG MO KIO AVE 10",  # Fine-grained location info
        "floor_area_sqm": 84,
        "lease_commence_date": "1985",
        "remaining_lease": "59 years 11 months"
    }

    pred, features_used, processed = predict_house_price(sample_input)

    # Print all columns of the final features and processed input.
    print("Predicted House Price:", pred)
    print("\nFinal Features used for prediction:")
    print(features_used.to_string(index=False))
    print("\nProcessed Input Data:")
    print(processed.to_string(index=False))

    # Compute SHAP explanation for the prediction.
    model, _, _ = load_artifacts()
    shap_df = compute_shap_explanation(model, features_used)
    print("\nInput Variable Importance (SHAP values) for the prediction:")
    print(shap_df.to_string(index=False))

    # Optional: Create an interactive force plot (requires Jupyter or appropriate front-end).
    # Uncomment the lines below to generate and save the force plot.
    # shap.initjs()
    # force_plot = shap.force_plot(shap.TreeExplainer(model).expected_value, shap_df['SHAP Value'].values, features_used.iloc[0, :])
    # shap.save_html("shap_force_plot.html", force_plot)
    # print("\nSHAP force plot saved to shap_force_plot.html")
