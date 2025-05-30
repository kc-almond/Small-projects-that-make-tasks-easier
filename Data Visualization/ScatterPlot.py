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
# Modify column names as per your CSV
df = pd.read_csv(csv_path)

# These should be the exact column headers from your CSV
x_col = "GA Vs30"      # Replace with your actual GA-derived 3CMT Vs30 column name
y_col = "ReMi VS30 (Theo)"    # Replace with your actual ReMi Vs30 column name

if x_col not in df.columns or y_col not in df.columns:
    raise ValueError(f"Columns '{x_col}' and/or '{y_col}' not found in the CSV file.")

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

# Fixed plot bounds and 1:1 reference line
min_val = 0
max_val = 800
plt.xlim(0, 800)
plt.ylim(0, 800)
plt.plot([0, 800], [0, 800], 'gray', linestyle='-', linewidth=1, label='1:1 Line')

# Equal aspect ratio and fixed ticks
plt.gca().set_aspect('equal', adjustable='box')
plt.xticks(np.arange(0, 801, 100))
plt.yticks(np.arange(0, 801, 100))

# Aspect ratio and equal increments
plt.gca().set_aspect('equal', adjustable='box')
tick_step = 100
plt.xticks(np.arange(0, max_val + tick_step, tick_step))
plt.yticks(np.arange(0, max_val + tick_step, tick_step))

# Labels and title
plt.xlabel("GA-Derived 3CMT Vs30 (m/s)")
plt.ylabel("ReMi Vs30 (m/s)")
plt.title("GA Vs30 vs ReMi VS30 Empirical Relationship")
plt.grid(True)
plt.legend()

# R² text
plt.text(400, 200, f'$R^2 = {r2:.2f}$', fontsize=12)

plt.tight_layout()
plt.show()
