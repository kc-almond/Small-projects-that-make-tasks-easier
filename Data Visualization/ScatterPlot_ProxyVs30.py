import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os

# === USER INPUT ===
csv_path = input("Enter path to CSV file: ").strip()

# Check if file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found: {csv_path}")

# === DATA LOADING ===
df = pd.read_csv(csv_path)

# Modify these if your columns are different
x_col = "RASTERVALU"
y_col = "FIELD_VS30"

if x_col not in df.columns or y_col not in df.columns:
    raise ValueError(f"Columns '{x_col}' and/or '{y_col}' not found in the CSV file.")

# === FILTER OUT VALUES LESS THAN 0 ===
df = df[(df[x_col] >= 0) & (df[y_col] >= 0)]

x = df[x_col].values
y = df[y_col].values

# === LINEAR REGRESSION AND R² ===
model = LinearRegression()
model.fit(x.reshape(-1, 1), y)
y_pred = model.predict(x.reshape(-1, 1))
r2 = r2_score(y, y_pred)

# === PLOTTING ===
plt.figure(figsize=(6, 6))
plt.scatter(x, y, color='dodgerblue', alpha=0.7, label='Data Points')

# Expanded plot bounds and 1:1 reference line
min_val = 0
max_val = 1500
plt.xlim(min_val, max_val)
plt.ylim(min_val, max_val)
plt.plot([min_val, max_val], [min_val, max_val], 'gray', linestyle='-', linewidth=1, label='1:1 Line')

# Equal aspect ratio and fixed ticks
plt.gca().set_aspect('equal', adjustable='box')
tick_step = 100
plt.xticks(np.arange(min_val, max_val + tick_step, tick_step))
plt.yticks(np.arange(min_val, max_val + tick_step, tick_step))

# Labels and title
plt.xlabel("Proxy Vs30 (m/s)")
plt.ylabel("Measured Vs30 (m/s)")
plt.title("Proxy vs Measured Vs30")
plt.grid(True)
plt.legend()

# Optional: R² annotation
# plt.text(800, 200, f'$R^2 = {r2:.2f}$', fontsize=12)

plt.tight_layout()
plt.show()
