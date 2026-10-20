import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import (
    RBF, Matern, RationalQuadratic, ExpSineSquared, ConstantKernel as C, WhiteKernel, DotProduct
)
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Step 1: Load Data
df = pd.read_csv('uyo_msw_data.csv')
print("Dataset Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Step 2: Preprocess & Feature Engineering
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date').reset_index(drop=True)

df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['time_index'] = np.arange(len(df))

# Cyclical month features for seasonality
df['sin_month'] = np.sin(2 * np.pi * df['month'] / 12.0)
df['cos_month'] = np.cos(2 * np.pi * df['month'] / 12.0)

# Holiday count feature
df['num_holidays'] = df['public_holidays'].fillna('').apply(
    lambda x: len(str(x).split(';')) if str(x).strip() != '' else 0
)

# Feature matrix X and target y
feature_cols = [
    'time_index', 'year', 'month', 'sin_month', 'cos_month',
    'avg_temperature_c', 'rainfall_mm', 'humidity_percent',
    'population', 'num_holidays'
]
X = df[feature_cols].copy()
y = df['waste_tonnes_estimated'].values

# Step 4: Chronological Train-Test Split (80% train, 20% test)
split_idx = int(len(df) * 0.8)
X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]
dates_train, dates_test = df['date'].iloc[:split_idx], df['date'].iloc[split_idx:]

print(f"Train samples: {len(X_train)} ({dates_train.iloc[0].strftime('%Y-%m')} to {dates_train.iloc[-1].strftime('%Y-%m')})")
print(f"Test samples: {len(X_test)} ({dates_test.iloc[0].strftime('%Y-%m')} to {dates_test.iloc[-1].strftime('%Y-%m')})")

# Feature Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define Candidate Kernels
kernels = {
    "RBF + WhiteKernel": (
        C(1.0, (1e-3, 1e3)) * RBF(length_scale=1.0, length_scale_bounds=(1e-2, 1e3)) 
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e1))
    ),
    "Matérn (nu=1.5) + WhiteKernel": (
        C(1.0, (1e-3, 1e3)) * Matern(length_scale=1.0, length_scale_bounds=(1e-2, 1e3), nu=1.5)
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e1))
    ),
    "Matérn (nu=2.5) + WhiteKernel": (
        C(1.0, (1e-3, 1e3)) * Matern(length_scale=1.0, length_scale_bounds=(1e-2, 1e3), nu=2.5)
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e1))
    ),
    "RationalQuadratic + WhiteKernel": (
        C(1.0, (1e-3, 1e3)) * RationalQuadratic(length_scale=1.0, alpha=1.0)
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e1))
    ),
    "Composite (Trend + RBF + WhiteKernel)": (
        C(1.0, (1e-3, 1e3)) * DotProduct(sigma_0=1.0) 
        + C(1.0, (1e-3, 1e3)) * RBF(length_scale=1.0) 
        + WhiteKernel(noise_level=1e-2, noise_level_bounds=(1e-5, 1e1))
    )
}

def evaluate_predictions(y_true, y_pred, y_std):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100.0
    r2 = r2_score(y_true, y_pred)
    
    # 95% Confidence Interval Coverage: [y_pred - 1.96*y_std, y_pred + 1.96*y_std]
    ci_lower = y_pred - 1.96 * y_std
    ci_upper = y_pred + 1.96 * y_std
    ci_coverage = np.mean((y_true >= ci_lower) & (y_true <= ci_upper)) * 100.0
    
    return {
        'MSE': mse,
        'RMSE': rmse,
        'MAE': mae,
        'MAPE (%)': mape,
        'R2': r2,
        '95% CI Coverage (%)': ci_coverage
    }

print("\n--- Model Evaluation on Test Set ---")
results = {}
for name, kernel in kernels.items():
    gpr = GaussianProcessRegressor(
        kernel=kernel,
        normalize_y=True,
        n_restarts_optimizer=15,
        random_state=42
    )
    gpr.fit(X_train_scaled, y_train)
    y_pred, y_std = gpr.predict(X_test_scaled, return_std=True)
    res = evaluate_predictions(y_test, y_pred, y_std)
    results[name] = (res, gpr)
    print(f"\nKernel: {name}")
    for metric, val in res.items():
        print(f"  {metric:20s}: {val:10.4f}")


