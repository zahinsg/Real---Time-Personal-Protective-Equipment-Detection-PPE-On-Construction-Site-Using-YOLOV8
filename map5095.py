import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV data
df = pd.read_csv(r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train16\results.csv")  # Replace with your file path if needed

# Ensure epoch starts at 1 for plotting
df['epoch'] = df.index + 1

# Create a figure with two subplots
plt.figure(figsize=(14, 6))

# Subplot 1: mAP50 and mAP50-95 trends
plt.subplot(1, 2, 1)
plt.plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP50', marker='o', markersize=4)
plt.plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP50-95', marker='s', markersize=4)
plt.title('mAP Trends Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('mAP Value')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Subplot 2: Moving averages (5-epoch window) to smooth noise
plt.subplot(1, 2, 2)
window = 5
df['mAP50_smooth'] = df['metrics/mAP50(B)'].rolling(window=window).mean()
df['mAP50-95_smooth'] = df['metrics/mAP50-95(B)'].rolling(window=window).mean()

plt.plot(df['epoch'], df['mAP50_smooth'], label=f'mAP50 (Smooth {window}-epoch)', color='blue', linestyle='--')
plt.plot(df['epoch'], df['mAP50-95_smooth'], label=f'mAP50-95 (Smooth {window}-epoch)', color='orange', linestyle='--')
plt.title('Smoothed mAP Trends (Reducing Noise)')
plt.xlabel('Epoch')
plt.ylabel('Smoothed mAP')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.show()

# Key Metrics Analysis
best_epoch_mAP50 = df['metrics/mAP50(B)'].idxmax() + 1
best_mAP50 = df['metrics/mAP50(B)'].max()
best_epoch_mAP50_95 = df['metrics/mAP50-95(B)'].idxmax() + 1
best_mAP50_95 = df['metrics/mAP50-95(B)'].max()

print("\n=== Key Insights ===")
print(f"1. Best mAP50: {best_mAP50:.4f} at epoch {best_epoch_mAP50}")
print(f"2. Best mAP50-95: {best_mAP50_95:.4f} at epoch {best_epoch_mAP50_95}")
print(f"3. Final mAP50: {df['metrics/mAP50(B)'].iloc[-1]:.4f} (Epoch {df['epoch'].iloc[-1]})")
print(f"4. Final mAP50-95: {df['metrics/mAP50-95(B)'].iloc[-1]:.4f} (Epoch {df['epoch'].iloc[-1]})")

# Growth Analysis
initial_mAP50 = df['metrics/mAP50(B)'].iloc[0]
final_mAP50 = df['metrics/mAP50(B)'].iloc[-1]
improvement_pct = ((final_mAP50 - initial_mAP50) / initial_mAP50) * 100
print(f"\n5. mAP50 improved by {improvement_pct:.2f}% from epoch 1 to {df['epoch'].iloc[-1]}")

# Stability Check (last 20 epochs)
last_20_epochs = df.tail(20)
mAP50_std = last_20_epochs['metrics/mAP50(B)'].std()
mAP50_95_std = last_20_epochs['metrics/mAP50-95(B)'].std()
print(f"\n6. Stability in last 20 epochs:")
print(f"   - mAP50 stddev: {mAP50_std:.4f} (lower = more stable)")
print(f"   - mAP50-95 stddev: {mAP50_95_std:.4f} (lower = more stable)")

# Suggested Early Stopping Point
suggested_epoch = best_epoch_mAP50_95  # Or use a plateau detection method
print(f"\n7. Suggested early stopping point: Epoch {suggested_epoch} (peak mAP50-95)")