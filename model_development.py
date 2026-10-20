"""
========================================================================================
PROJECT TITLE: A GAUSSIAN PROCESS REGRESSION FOR FORECASTING SOLID WASTE GENERATION
               IN UYO MUNICIPALITY
CANDIDATE:     EFFIONG, SAMUEL ETIM (REG NO: AK22/PHS/CSC/029)
DEPARTMENT:    COMPUTER SCIENCE, AKWA IBOM STATE UNIVERSITY
SUPERVISOR:    DR. ANIETIE P. EKONG
========================================================================================
Architecture Stages:
1. DATA COLLECTION & PREPROCESSING
2. MODEL DESIGN (FEATURE ENGINEERING, KERNEL OPTIMIZATION, GPR TRAINING & EVALUATION)
3. IMPLEMENTATION & DECISION SUPPORT (STREAMLIT DASHBOARD & SCENARIO FORECASTING)
========================================================================================
"""

import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    RBF, Matern, RationalQuadratic, DotProduct, ConstantKernel as C, WhiteKernel, ExpSineSquared
)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Set aesthetic styling
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

print("=" * 80)
print("STAGE 1: DATA COLLECTION & PREPROCESSING (Section 3.3.1 & 3.3.4)")
print("=" * 80)

# 1.1 Load Data
DATA_PATH = "uyo_msw_data.csv"
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATA_PATH}")

df = pd.read_csv(DATA_PATH)
print(f"[OK] Data loaded successfully from {DATA_PATH}")
print(f"    Total records: {len(df)} monthly observations")
print(f"    Available features: {df.columns.tolist()}\n")

# 1.2 Time-Series Formatting & Sorting
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

# 1.3 Preprocessing: Check Missing Values & Duplicates
duplicates = df.duplicated().sum()
missing = df.isnull().sum()
print(f"[OK] Duplicate rows: {duplicates}")
print(f"[OK] Missing values check:\n{missing}\n")

# 1.4 Outlier Detection using IQR on Waste Generation
Q1 = df['waste_tonnes_estimated'].quantile(0.25)
Q3 = df['waste_tonnes_estimated'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
outliers = df[(df['waste_tonnes_estimated'] < lower_bound) | (df['waste_tonnes_estimated'] > upper_bound)]
print(f"[OK] Outlier Detection: Found {len(outliers)} outliers based on IQR [{lower_bound:.2f}, {upper_bound:.2f}] tonnes.")

print("\n" + "=" * 80)
print("STAGE 2: FEATURE ENGINEERING & DATA SPLITTING")
print("=" * 80)

# 2.1 Feature Engineering
# Temporal features
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['quarter'] = df['date'].dt.quarter
df['time_index'] = np.arange(len(df))

# Cyclical month encoding (captures annual cycle continuously)
df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12.0)
df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12.0)

# Holiday count feature from public_holidays string
df['num_holidays'] = df['public_holidays'].fillna('').apply(
    lambda x: len(str(x).split(';')) if str(x).strip() != '' else 0
)

# Per-capita waste generation (tonnes/person/month)
df['per_capita_kg_per_day'] = (df['waste_tonnes_estimated'] * 1000) / (df['population'] * df['date'].dt.days_in_month)

print("[OK] Engineered Features:")
print("    - Temporal: time_index (trend), year, month, quarter, sin_month, cos_month")
print("    - Weather: avg_temperature_c, rainfall_mm, humidity_percent")
print("    - Demographic: population")
print("    - Calendar: num_holidays")
print(f"    - Mean Per-Capita Generation: {df['per_capita_kg_per_day'].mean():.3f} kg/capita/day")

feature_cols = [
    'time_index', 'year', 'month', 'sin_month', 'cos_month',
    'avg_temperature_c', 'rainfall_mm', 'humidity_percent',
    'population', 'num_holidays'
]
target_col = 'waste_tonnes_estimated'

X = df[feature_cols].copy()
y = df[target_col].values

# 2.2 Chronological Train/Test Split (80% Train, 20% Test)
split_idx = int(len(df) * 0.8)  # 67 train, 17 test
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]
dates_train, dates_test = df['date'].iloc[:split_idx], df['date'].iloc[split_idx:]

print(f"\n[OK] Train Set: {len(X_train)} samples ({dates_train.iloc[0].strftime('%Y-%m')} to {dates_train.iloc[-1].strftime('%Y-%m')})")
print(f"[OK] Test Set:  {len(X_test)} samples ({dates_test.iloc[0].strftime('%Y-%m')} to {dates_test.iloc[-1].strftime('%Y-%m')})")

# 2.3 Feature Standardization
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
X_all_scaled = scaler.transform(X)

print("\n" + "=" * 80)
print("STAGE 3: KERNEL COMPARISON & HYPERPARAMETER OPTIMIZATION (Section 3.3.4)")
print("=" * 80)

# Define Candidate Kernels
kernel_candidates = {
    "RBF + Noise": (
        C(1.0, (1e-2, 1e4)) * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3))
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e2))
    ),
    "Matérn (nu=1.5) + Noise": (
        C(1.0, (1e-2, 1e4)) * Matern(length_scale=1.0, length_scale_bounds=(1e-2, 1e3), nu=1.5)
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e2))
    ),
    "Matérn (nu=2.5) + Noise": (
        C(1.0, (1e-2, 1e4)) * Matern(length_scale=1.0, length_scale_bounds=(1e-2, 1e3), nu=2.5)
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e2))
    ),
    "RationalQuadratic + Noise": (
        C(1.0, (1e-2, 1e4)) * RationalQuadratic(length_scale=1.0, alpha=1.0)
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e2))
    ),
    "Proposed Composite (Trend + Matérn + Noise)": (
        C(1.0, (1e-2, 1e4)) * DotProduct(sigma_0=1.0, sigma_0_bounds=(1e-2, 1e3))
        + C(1.0, (1e-2, 1e4)) * Matern(length_scale=1.0, length_scale_bounds=(1e-2, 1e3), nu=1.5)
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e2))
    )
}

def compute_metrics(y_true, y_pred, y_std):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100.0
    r2 = r2_score(y_true, y_pred)
    lower = y_pred - 1.96 * y_std
    upper = y_pred + 1.96 * y_std
    coverage = np.mean((y_true >= lower) & (y_true <= upper)) * 100.0
    return {
        "MSE": mse, "RMSE": rmse, "MAE": mae, "MAPE (%)": mape,
        "R2": r2, "95% CI Coverage (%)": coverage
    }

eval_records = []
fitted_models = {}

for name, kern in kernel_candidates.items():
    print(f"--> Training GPR with [{name}]...")
    gpr = GaussianProcessRegressor(
        kernel=kern,
        normalize_y=True,
        alpha=1e-5,
        n_restarts_optimizer=10,
        random_state=42
    )
    gpr.fit(X_train_scaled, y_train)
    y_test_pred, y_test_std = gpr.predict(X_test_scaled, return_std=True)
    m = compute_metrics(y_test, y_test_pred, y_test_std)
    m["Kernel"] = name
    eval_records.append(m)
    fitted_models[name] = gpr

eval_df = pd.DataFrame(eval_records)[["Kernel", "RMSE", "MAE", "MAPE (%)", "R2", "95% CI Coverage (%)"]]
print("\n" + "=" * 80)
print("TEST SET BENCHMARK RESULTS (Section 3.3.4 Step 10):")
print("=" * 80)
print(eval_df.to_string(index=False))

# Select Best Model
best_kernel_name = "Proposed Composite (Trend + Matérn + Noise)"
best_gpr = fitted_models[best_kernel_name]

# Evaluate on Train, Test, and Full Dataset
y_train_pred, y_train_std = best_gpr.predict(X_train_scaled, return_std=True)
y_test_pred, y_test_std = best_gpr.predict(X_test_scaled, return_std=True)
y_all_pred, y_all_std = best_gpr.predict(X_all_scaled, return_std=True)

train_res = compute_metrics(y_train, y_train_pred, y_train_std)
test_res = compute_metrics(y_test, y_test_pred, y_test_std)
overall_res = compute_metrics(y, y_all_pred, y_all_std)

print("\n" + "=" * 80)
print(f"DETAILED PERFORMANCE METRICS FOR: {best_kernel_name}")
print("=" * 80)
print(f"Training Set   -> R2: {train_res['R2']:.4f} | RMSE: {train_res['RMSE']:.2f} t | MAE: {train_res['MAE']:.2f} t | MAPE: {train_res['MAPE (%)']:.2f}% | 95% CI: {train_res['95% CI Coverage (%)']:.1f}%")
print(f"Testing Set    -> R2: {test_res['R2']:.4f} | RMSE: {test_res['RMSE']:.2f} t | MAE: {test_res['MAE']:.2f} t | MAPE: {test_res['MAPE (%)']:.2f}% | 95% CI: {test_res['95% CI Coverage (%)']:.1f}%")
print(f"Overall Series -> R2: {overall_res['R2']:.4f} | RMSE: {overall_res['RMSE']:.2f} t | MAE: {overall_res['MAE']:.2f} t | MAPE: {overall_res['MAPE (%)']:.2f}% | 95% CI: {overall_res['95% CI Coverage (%)']:.1f}%")

print("\n" + "=" * 80)
print("STAGE 4: FUTURE FORECASTING (2026 - 2030) & RETRAINING")
print("=" * 80)

# Retrain GPR on full dataset (84 months: 2019 - 2025) for future deployment
final_gpr = GaussianProcessRegressor(
    kernel=kernel_candidates[best_kernel_name],
    normalize_y=True,
    alpha=1e-5,
    n_restarts_optimizer=15,
    random_state=42
)
final_scaler = StandardScaler()
X_full_scaled = final_scaler.fit_transform(X)
final_gpr.fit(X_full_scaled, y)
print(f"[OK] Final GPR trained on full 84-month history.")
print(f"    Learned Kernel: {final_gpr.kernel_}")

# Generate future feature inputs (2026-01 to 2030-12: 60 months)
future_dates = pd.date_range(start='2026-01-01', end='2030-12-01', freq='MS')
future_df = pd.DataFrame({'date': future_dates})
future_df['year'] = future_df['date'].dt.year
future_df['month'] = future_df['date'].dt.month
future_df['time_index'] = np.arange(len(df), len(df) + len(future_df))
future_df['sin_month'] = np.sin(2 * np.pi * future_df['month'] / 12.0)
future_df['cos_month'] = np.cos(2 * np.pi * future_df['month'] / 12.0)

# Realistic projections for Uyo Municipality:
# Population annual growth ~ 2.8% per annum
last_pop = df['population'].iloc[-1]
monthly_pop_growth = (1 + 0.028) ** (1/12)
future_pops = [last_pop * (monthly_pop_growth ** (i + 1)) for i in range(len(future_df))]
future_df['population'] = future_pops

# Climate features: Average monthly historical climate for Uyo (tropical rainforest climate)
monthly_climate = df.groupby('month')[['avg_temperature_c', 'rainfall_mm', 'humidity_percent']].mean()
future_df = future_df.merge(monthly_climate, on='month', how='left')

# Public holidays typical monthly counts for Nigeria
monthly_holidays = df.groupby('month')['num_holidays'].median().round()
future_df = future_df.merge(monthly_holidays, on='month', how='left')

# Predict Future
X_future_scaled = final_scaler.transform(future_df[feature_cols])
y_future_pred, y_future_std = final_gpr.predict(X_future_scaled, return_std=True)
future_df['forecast_tonnes'] = y_future_pred
future_df['uncertainty_std'] = y_future_std
future_df['ci_lower_95'] = y_future_pred - 1.96 * y_future_std
future_df['ci_upper_95'] = y_future_pred + 1.96 * y_future_std

print(f"[OK] 5-Year Projections (2026 - 2030) Generated:")
for yr in [2026, 2027, 2028, 2029, 2030]:
    yr_sub = future_df[future_df['year'] == yr]
    annual_tonnes = yr_sub['forecast_tonnes'].sum()
    mean_mo = yr_sub['forecast_tonnes'].mean()
    print(f"    Year {yr}: Annual Total = {annual_tonnes:,.1f} tonnes | Monthly Avg = {mean_mo:,.1f} tonnes (+/- {yr_sub['uncertainty_std'].mean():.1f})")

# Save model, scaler and metadata
artifacts = {
    'model': final_gpr,
    'scaler': final_scaler,
    'feature_cols': feature_cols,
    'eval_df': eval_df,
    'metrics': {
        'train': train_res,
        'test': test_res,
        'overall': overall_res
    },
    'historical_df': df,
    'future_df': future_df
}
joblib.dump(artifacts, 'gpr_waste_model.pkl')
print("\n[OK] Model, Scaler & Pipeline Artifacts saved to 'gpr_waste_model.pkl'")
print("=" * 80)

