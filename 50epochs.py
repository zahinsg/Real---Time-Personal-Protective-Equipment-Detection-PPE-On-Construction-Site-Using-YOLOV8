import pandas as pd
import matplotlib.pyplot as plt

# Set your CSV file path here
csv_path = r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train\results 1.csv"

# Load the CSV data
df = pd.read_csv(csv_path)

# Filter only the first 50 epochs
df_50 = df[df["epoch"] <= 50]

# Define columns to plot
plot_columns = [
    ("train/box_loss", "train/box_loss"),
    ("train/cls_loss", "train/cls_loss"),
    ("train/dfl_loss", "train/dfl_loss"),
    ("metrics/precision(B)", "metrics/precision(B)"),
    ("metrics/recall(B)", "metrics/recall(B)"),
    ("val/box_loss", "val/box_loss"),
    ("val/cls_loss", "val/cls_loss"),
    ("val/dfl_loss", "val/dfl_loss"),
    ("metrics/mAP50(B)", "metrics/mAP50(B)"),
    ("metrics/mAP50-95(B)", "metrics/mAP50-95(B)")
]

# Plot the graphs
fig, axs = plt.subplots(2, 5, figsize=(20, 10))
axs = axs.flatten()

for i, (col, title) in enumerate(plot_columns):
    axs[i].plot(df_50["epoch"], df_50[col], label="results", marker='o', color='blue')
    axs[i].plot(df_50["epoch"], df_50[col].rolling(window=5).mean(), linestyle='dotted', label="smooth", color='orange')
    axs[i].set_title(title)
    axs[i].legend()

plt.tight_layout()
plt.show()
