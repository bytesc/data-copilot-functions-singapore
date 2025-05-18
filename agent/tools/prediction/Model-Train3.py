#!/usr/bin/env python3
"""
Model Training Script for HDB House Price Prediction

Features:
1. Data Loading from multiple CSV files.
2. Extended Location Features: For "town", beyond target encoding, aggregated statistics (mean, median, std, count)
   are computed on the derived target (price per sqm) from the training set and merged back.
3. Inclusion of fine-grained location (street_name) using categorical (target) encoding.
4. Feature engineering for time-related features.
5. Improved XGBoost hyperparameters for a larger training set.
6. Saving of trained model and target encoder for deployment.
"""

import os
import glob
import pandas as pd
import numpy as np
import matplotlib
# Set backend for plotting; you can try 'TkAgg' or 'Qt5Agg' as needed.
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from xgboost import XGBRegressor, plot_importance
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib  # For saving and loading the model
import category_encoders as ce  # For target encoding

# -------------------------------
# 1. Data Loading and Preprocessing
# -------------------------------
# Adjust the glob pattern as needed (e.g., CSV files stored in "Resale Transations/" folder).
# Locate all CSV files (adjust the path if needed)
csv_files = glob.glob("Resale Transations/*.csv")
if not csv_files:
    raise ValueError("No CSV files found in the specified folder.")
print("Loading CSV files:", csv_files)

df_list = []
for file in csv_files:
    df_tmp = pd.read_csv(file)

    # If the file is missing 'remaining_lease', create it.
    if 'remaining_lease' not in df_tmp.columns:
        # Check if the necessary columns exist.
        if 'lease_commence_date' in df_tmp.columns and 'month' in df_tmp.columns:
            # Convert 'lease_commence_date' to numeric (if needed)
            df_tmp['lease_commence_date'] = pd.to_numeric(df_tmp['lease_commence_date'], errors='coerce')
            # Convert 'month' to datetime (assumed to be in "YYYY-MM" format)
            df_tmp['month'] = pd.to_datetime(df_tmp['month'], format='%Y-%m', errors='coerce')
            # Compute remaining_lease based on a 99-year lease:
            # (lease_commence_date + 99) - (transaction year)
            df_tmp['remaining_lease'] = (df_tmp['lease_commence_date'] + 99) - df_tmp['month'].dt.year
        else:
            # If the necessary information is missing, fill the column with NaN.
            df_tmp['remaining_lease'] = np.nan

    df_list.append(df_tmp)

# Concatenate all CSVs into one DataFrame.
df = pd.concat(df_list, ignore_index=True)

# Inspect unique values in 'month' column to verify its format.
print("Unique values in 'month' column:")
print(df['month'].unique())

# Convert 'month' (format "YYYY-MM") to datetime.
df['month'] = pd.to_datetime(df['month'], format='%Y-%m', errors='coerce')
print("Date range in dataset:", df['month'].min(), "to", df['month'].max())

# Drop rows where 'month' conversion failed.
df = df.dropna(subset=['month'])

# Retain "street_name" (do NOT drop it) since we want to use fine-grained location info.
# If there are columns considered irrelevant besides "block", drop them:
if 'block' in df.columns:
    df.drop(columns=['block'], inplace=True)

# -------------------------------
# Preserve Floor Range and Other Important Factors
# -------------------------------
def convert_storey_range(s):
    try:
        lower, upper = s.split(" to ")
        return (int(lower) + int(upper)) / 2  # Midpoint as numeric representation.
    except Exception:
        return np.nan

if 'storey_range' in df.columns:
    df['storey_range_numeric'] = df['storey_range'].apply(convert_storey_range)
else:
    raise ValueError("The dataset must contain a 'storey_range' column.")

# Check for presence of important columns.
for col in ['floor_area_sqm', 'lease_commence_date', 'remaining_lease']:
    if col not in df.columns:
        raise ValueError(f"Important column '{col}' is missing from the dataset.")

# -------------------------------
# Derived Target: Price per Square Meter
# -------------------------------
df['price_per_sqm'] = df['resale_price'] / df['floor_area_sqm']

# -------------------------------
# 2. Time-Based Split
# -------------------------------
# Use a cutoff date of July 1, 2024.
cutoff_date = pd.Timestamp("2024-07-01")
train_df = df[df['month'] < cutoff_date].copy()
test_df  = df[df['month'] >= cutoff_date].copy()

print(f"\nTraining set size: {train_df.shape}")
print(f"Testing set size: {test_df.shape}")

if train_df.empty or test_df.empty:
    raise ValueError("One of the time-based splits is empty. Please adjust your cutoff date.")

# -------------------------------
# 2.5 Add Extended 'Town' Features (Aggregated Statistics)
# -------------------------------
# Compute aggregated statistics for "town" using the training data and the derived target "price_per_sqm"
town_stats_df = train_df.groupby("town")["price_per_sqm"].agg(['mean', 'median', 'std', 'count']).reset_index()
town_stats_df.rename(columns={
    'mean': 'town_mean',
    'median': 'town_median',
    'std': 'town_std',
    'count': 'town_count'
}, inplace=True)

# Convert the aggregated DataFrame into a dictionary.
# Town names are converted to uppercase for consistent lookup later.
town_stats_dict = {}
for _, row in town_stats_df.iterrows():
    town_key = str(row['town']).upper()
    town_stats_dict[town_key] = {
        'town_mean': row['town_mean'],
        'town_median': row['town_median'],
        'town_std': row['town_std'],
        'town_count': row['town_count']
    }

# Save the town aggregated statistics dictionary to a file using joblib.
joblib.dump(town_stats_dict, "town_stats.joblib")
print("Town aggregated statistics saved to town_stats.joblib")

# Merge these aggregated statistics back into both training and test sets on the "town" column.
train_df = pd.merge(train_df, town_stats_df, on='town', how='left')
test_df = pd.merge(test_df, town_stats_df, on='town', how='left')

# -------------------------------
# 3. Define Features and Target
# -------------------------------
target_variable = 'resale_price'
if target_variable not in df.columns:
    raise ValueError(f"Target column '{target_variable}' not found.")

# We now plan to use:
# - For location:
#     * The original "town" (target encoded) plus extended aggregated features for town:
#         'town_mean', 'town_median', 'town_std', 'town_count'
#     * "street_name" as an additional fine-grained categorical feature.
# - Other categorical features: 'flat_type', 'flat_model'
# - Numeric features: 'storey_range_numeric', 'floor_area_sqm', 'lease_commence_date', 'remaining_lease'
# - Time-based features: derived from "month": 'year', 'month_sin', 'month_cos'
#
# Preserve original string columns for final output as needed.
X_train = train_df.copy()
X_test = test_df.copy()

# Keep a copy of original columns for output.
X_test_output = X_test.copy()

# -------------------------------
# 4. Engineer Time-Based Features
# -------------------------------
# Extract year and month number from 'month'
X_train['year'] = X_train['month'].dt.year
X_train['month_num'] = X_train['month'].dt.month
X_test['year'] = X_test['month'].dt.year
X_test['month_num'] = X_test['month'].dt.month

# Create cyclical (sin and cos) features.
X_train['month_sin'] = np.sin(2 * np.pi * X_train['month_num'] / 12)
X_train['month_cos'] = np.cos(2 * np.pi * X_train['month_num'] / 12)
X_test['month_sin'] = np.sin(2 * np.pi * X_test['month_num'] / 12)
X_test['month_cos'] = np.cos(2 * np.pi * X_test['month_num'] / 12)

# Drop raw 'month' and 'month_num' columns (they are no longer needed for modeling).
X_train.drop(columns=['month', 'month_num'], inplace=True)
X_test.drop(columns=['month', 'month_num'], inplace=True)

# -------------------------------
# Convert Lease-related Columns to Numeric
# -------------------------------
# Convert lease_commence_date (e.g., the year) to numeric.
X_train['lease_commence_date'] = pd.to_numeric(X_train['lease_commence_date'], errors='coerce')
X_test['lease_commence_date'] = pd.to_numeric(X_test['lease_commence_date'], errors='coerce')

# Convert remaining_lease from "XX years YY months" to numeric (years).
def convert_remaining_lease(s):
    try:
        parts = s.split()
        years = int(parts[0])
        months = int(parts[2])
        return years + months / 12.0
    except Exception:
        return np.nan

X_train['remaining_lease'] = X_train['remaining_lease'].apply(lambda x: convert_remaining_lease(x) if isinstance(x, str) else x)
X_test['remaining_lease'] = X_test['remaining_lease'].apply(lambda x: convert_remaining_lease(x) if isinstance(x, str) else x)

# -------------------------------
# 5. Categorical Encoding
# -------------------------------
# Define categorical columns for target encoding.
# Here we include: "town", "flat_type", "flat_model", and "street_name".
cat_cols = ['town', 'flat_type', 'flat_model', 'street_name']

# Fill missing values with "unknown" for these columns.
for col in cat_cols:
    X_train[col] = X_train[col].fillna("unknown")
    X_test[col] = X_test[col].fillna("unknown")

# Instantiate and apply the target encoder using the derived target "price_per_sqm".
encoder = ce.TargetEncoder(cols=cat_cols)
X_train[cat_cols] = encoder.fit_transform(X_train[cat_cols], X_train['price_per_sqm'])
X_test[cat_cols] = encoder.transform(X_test[cat_cols])

# -------------------------------
# 6. Final Feature Selection for Modeling
# -------------------------------
# Final features include:
# - Categorical (target encoded): 'town', 'flat_type', 'flat_model', 'street_name'
# - Extended town features: 'town_mean', 'town_median', 'town_std', 'town_count'
# - Other numeric features: 'storey_range_numeric', 'floor_area_sqm', 'lease_commence_date', 'remaining_lease'
# - Time-based features: 'year', 'month_sin', 'month_cos'
features = [
    'town', 'flat_type', 'flat_model', 'street_name',
    'town_mean', 'town_median', 'town_std', 'town_count',
    'storey_range_numeric', 'floor_area_sqm', 'lease_commence_date', 'remaining_lease',
    'year', 'month_sin', 'month_cos'
]

X_train_model = X_train[features]
X_test_model = X_test[features]

y_train = X_train[target_variable]
y_test = X_test[target_variable]

print("\nFeatures used for modeling:")
print(X_train_model.columns.tolist())

# -------------------------------
# 7. Correlation Analysis on Training Data
# -------------------------------
train_corr = X_train_model.copy()
train_corr[target_variable] = y_train

correlations = train_corr.corr()[target_variable].drop(target_variable).sort_values(ascending=False)
print("\nFeature Correlations with House Price (resale_price) on Training Data:")
print(correlations)

correlations.to_csv("feature_correlations.csv", header=['Correlation'])

# -------------------------------
# 8. Model Training with Improved Parameters
# -------------------------------
# Using additional regularization/hyperparameter tuning for a larger dataset.
model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train_model, y_train)
print("\nXGBoost model training complete.")

# -------------------------------
# 9. Model Validation and Evaluation
# -------------------------------
y_pred = model.predict(X_test_model)

mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("\nValidation Metrics:")
print("MAPE: {:.2f}%".format(mape))
print("MSE: {:.2f}".format(mse))
print("RMSE: {:.2f}".format(rmse))
print("R²: {:.2f}".format(r2))

plt.figure(figsize=(8,6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.title("Actual vs Predicted Resale Prices")
plt.xlabel("Actual Resale Price")
plt.ylabel("Predicted Resale Price")
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
plt.grid(True)
plt.show()

plt.figure(figsize=(10,8))
plot_importance(model, max_num_features=10)
plt.title("Top 10 Feature Importances")
plt.show()

# -------------------------------
# 10. Output Processed Validation Data with Predictions
# -------------------------------
validation_results = X_test_model.copy()
validation_results['predicted_resale_price'] = y_pred
validation_results['actual_resale_price'] = y_test.values

# Add back original columns for human-readability.
validation_results['month'] = X_test_output['month'].dt.strftime('%Y-%m')
validation_results['storey_range'] = X_test_output['storey_range']
validation_results['floor_area_sqm'] = X_test_output['floor_area_sqm']
validation_results['lease_commence_date'] = X_test_output['lease_commence_date']
validation_results['remaining_lease'] = X_test_output['remaining_lease']

cols_order = [
    'month', 'storey_range',
    'town', 'flat_type', 'flat_model', 'street_name',
    'town_mean', 'town_median', 'town_std', 'town_count',
    'storey_range_numeric', 'floor_area_sqm', 'lease_commence_date', 'remaining_lease',
    'year', 'month_sin', 'month_cos',
    'actual_resale_price', 'predicted_resale_price'
]
validation_results = validation_results[cols_order]
output_csv = "validation_predictions.csv"
validation_results.to_csv(output_csv, index=False)
print(f"\nValidation dataset with predictions saved to: {output_csv}")

# -------------------------------
# 11. Save Artifacts for Deployment
# -------------------------------
model_file = "xgboost_house_price_model.joblib"
joblib.dump(model, model_file)
print("\nModel saved to:", model_file)

encoder_file = "target_encoder.joblib"
joblib.dump(encoder, encoder_file)
print("Target encoder saved to:", encoder_file)

# -------------------------------
# 12. (Optional) Model Deployment Example
# -------------------------------
loaded_model = joblib.load(model_file)
print("Model loaded for prediction.")

new_data = X_test_model.iloc[0:1]
predicted_price = loaded_model.predict(new_data)
print("\nPrediction for a new data point:")
print("Input features:\n", new_data)
print("Predicted resale price: {:.2f}".format(predicted_price[0]))
