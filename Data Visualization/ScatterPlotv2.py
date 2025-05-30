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

x_col = "GA Vs30"
y_col = "ReMi VS30 (Theo)"
class_col = "Site Class"

# Validate columns
for col in [x_col, y_col, class_col]:
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in the CSV file.")

# === LINEAR REGRESSION AND R² ===
x = df[x_col].values
y = df[y_col].values
model = LinearRegression()
model.fit(x.reshape(-1, 1), y)
y_pred = model.predict(x.reshape(-1, 1))
r2 = r2_score(y, y_pred)

# === COLOR AND MARKER SETTINGS BY SITE CLASS ===
site_colors = {
    'A': 'darkgreen',
    'B': 'blue',
    'C': 'orange',
    'D': 'red',
    'E': 'purple',
    'F': 'brown'
}

site_markers = {
    'A': 'D',   # Circle
    'B': 'v',   # Square
    'C': 'o',   # Diamond
    'D': 's',   # Triangle up
    'E': '^',   # Triangle down
    'F': 'P'    # Plus-filled
}

# === PLOTTING ===
plt.figure(figsize=(6, 6))

# Scatter each Site Class with its own color and marker
for site_class in df[class_col].unique():
    class_df = df[df[class_col] == site_class]
    plt.scatter(
        class_df[x_col],
        class_df[y_col],
        label=f'Site Class {site_class}',
        color=site_colors.get(site_class, 'gray'),
        marker=site_markers.get(site_class, 'o'),
        alpha=0.7,
        edgecolors='black',
        linewidths=0.5
    )

# === 1:1 Reference Line ===
plt.plot([0, 800], [0, 800], 'gray', linestyle='-', linewidth=1, label='1:1 Line')

# === FIXED AXES, LABELS, AND TICKS ===
plt.xlim(0, 800)
plt.ylim(0, 800)
plt.gca().set_aspect('equal', adjustable='box')
plt.xticks(np.arange(0, 801, 100))
plt.yticks(np.arange(0, 801, 100))
plt.grid(True)

# === LABELS AND TITLE ===
plt.xlabel("GA-Derived 3CMT Vs30 (m/s)")
plt.ylabel("ReMi Vs30 (m/s)")
plt.title("GA Vs30 vs ReMi Vs30 by Site Class")

# === R² LABEL === Remove # to unhide
#plt.text(400, 200, f'$R^2 = {r2:.2f}$', fontsize=12)

# === LEGEND AND SHOW ===
plt.legend()
plt.tight_layout()
plt.show()
