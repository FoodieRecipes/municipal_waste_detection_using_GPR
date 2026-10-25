import joblib
import numpy as np
import pandas as pd

art = joblib.load('gpr_waste_model.pkl')
model = art['model']
scaler = art['scaler']
features = art['feature_cols']
df_hist = art['historical_df']
df_fut = art['future_df']

def predict_waste(year, month, pop, temp, rain, hum, hols):
    t_idx = (year - 2019) * 12 + (month - 1)
    sin_m = np.sin(2 * np.pi * month / 12.0)
    cos_m = np.cos(2 * np.pi * month / 12.0)
    row = pd.DataFrame([{
        'time_index': t_idx,
        'year': year,
        'month': month,
        'sin_month': sin_m,
        'cos_month': cos_m,
        'avg_temperature_c': temp,
        'rainfall_mm': rain,
        'humidity_percent': hum,
        'population': pop,
        'num_holidays': hols
    }])[features]
    scaled = scaler.transform(row)
    pred, std = model.predict(scaled, return_std=True)
    return pred[0], std[0]

print("--- Concrete Predictions Across Classes ---")
scenarios = [
    # Low Class (< 35,000 tonnes)
    ("Low (Baseline 2021 dry season)", 2021, 2, 510000, 28.0, 30.0, 75.0, 0),
    ("Low (2022 dry season)", 2022, 1, 530000, 27.5, 25.0, 76.0, 1),
    ("Low (Hypothetical low demographic / recession)", 2026, 1, 490000, 28.0, 15.0, 74.0, 0),
    
    # Moderate Class (35,000 - 40,000 tonnes)
    ("Moderate (2024 early dry month)", 2024, 3, 565000, 27.8, 80.0, 80.0, 1),
    ("Moderate (2025 dry season baseline)", 2025, 2, 585000, 27.5, 50.0, 78.0, 0),
    ("Moderate (2026 low rainfall / early month)", 2026, 2, 560000, 27.5, 45.0, 78.0, 0),
    
    # High Class (40,000 - 45,000 tonnes)
    ("High (2025 festive/wet)", 2025, 10, 592000, 26.0, 310.0, 88.0, 2),
    ("High (2026 standard projected month)", 2026, 5, 605000, 26.5, 240.0, 86.0, 1),
    ("High (2027 dry/transitional month)", 2027, 2, 620000, 27.5, 60.0, 79.0, 0),
    
    # Very High Class (>= 45,000 tonnes)
    ("Very High (2026 peak wet season)", 2026, 7, 607000, 25.5, 480.0, 91.0, 0),
    ("Very High (2026 festive peak)", 2026, 12, 615000, 26.8, 30.0, 78.0, 3),
    ("Very High (2028 baseline growth)", 2028, 6, 645000, 26.0, 350.0, 88.0, 1),
]

for name, y, m, pop, temp, rain, hum, hols in scenarios:
    p, s = predict_waste(y, m, pop, temp, rain, hum, hols)
    daily = p / 30.4167
    print(f"{name:45s} | Year {y} M{m:02d} | Pop: {pop:,} | Rain: {rain:5.1f}mm | Hols: {hols} => {p:,.1f} t ({daily:,.1f} t/d) [±{s:,.1f}]")

print("\n--- Sensitivity: Varying Individual Features around Base (2026 June: Pop 600k, Temp 26.5, Rain 200, Hum 86, Hols 1) ---")
base_p, _ = predict_waste(2026, 6, 600000, 26.5, 200, 86, 1)
print(f"Base Prediction: {base_p:,.1f} t")

print("\n1. Impact of Population:")
for pop in [480000, 520000, 560000, 600000, 640000, 680000]:
    p, _ = predict_waste(2026, 6, pop, 26.5, 200, 86, 1)
    diff = p - base_p
    c = "Very Low" if p < 30000 else "Low" if p < 35000 else "Moderate" if p < 40000 else "High" if p < 45000 else "Very High"
    print(f"   Pop: {pop:,} -> {p:,.1f} t (Diff: {diff:+,.1f} t) => Class: {c}")

print("\n2. Impact of Rainfall Depth (mm):")
for r in [10, 100, 250, 450, 650]:
    p, _ = predict_waste(2026, 6, 600000, 26.5, r, 86, 1)
    diff = p - base_p
    c = "Very Low" if p < 30000 else "Low" if p < 35000 else "Moderate" if p < 40000 else "High" if p < 45000 else "Very High"
    print(f"   Rain: {r:3d} mm -> {p:,.1f} t (Diff: {diff:+,.1f} t) => Class: {c}")

print("\n3. Impact of Public Holidays:")
for h in [0, 1, 2, 3, 4]:
    p, _ = predict_waste(2026, 6, 600000, 26.5, 200, 86, h)
    diff = p - base_p
    c = "Very Low" if p < 30000 else "Low" if p < 35000 else "Moderate" if p < 40000 else "High" if p < 45000 else "Very High"
    print(f"   Holidays: {h} -> {p:,.1f} t (Diff: {diff:+,.1f} t) => Class: {c}")

print("\n4. Impact of Ambient Temperature (°C):")
for t in [24.5, 26.0, 27.5, 29.0]:
    p, _ = predict_waste(2026, 6, 600000, t, 200, 86, 1)
    diff = p - base_p
    c = "Very Low" if p < 30000 else "Low" if p < 35000 else "Moderate" if p < 40000 else "High" if p < 45000 else "Very High"
    print(f"   Temp: {t:.1f}°C -> {p:,.1f} t (Diff: {diff:+,.1f} t) => Class: {c}")

print("\n5. Impact of Month (Harmonic Seasonality in 2026 with Month-Specific Typical Weather):")
for m in range(1, 13):
    typical_rain = df_hist[df_hist['month'] == m]['rainfall_mm'].mean()
    typical_temp = df_hist[df_hist['month'] == m]['avg_temperature_c'].mean()
    typical_hum = df_hist[df_hist['month'] == m]['humidity_percent'].mean()
    typical_hols = int(round(df_hist[df_hist['month'] == m]['num_holidays'].mean()))
    pop = 600000
    p, _ = predict_waste(2026, m, pop, typical_temp, typical_rain, typical_hum, typical_hols)
    c = "Very Low" if p < 30000 else "Low" if p < 35000 else "Moderate" if p < 40000 else "High" if p < 45000 else "Very High"
    print(f"   Month {m:02d} ({pd.to_datetime(f'2026-{m:02d}-01').strftime('%b')}) -> Rain: {typical_rain:5.1f}mm, Hols: {typical_hols} => {p:,.1f} t => Class: {c}")

