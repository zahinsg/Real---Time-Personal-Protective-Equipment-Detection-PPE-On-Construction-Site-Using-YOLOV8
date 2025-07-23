import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train9\results.csv')

# Plot training vs. validation losses
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.plot(df['epoch'], df['train/box_loss'], label='Train')
plt.plot(df['epoch'], df['val/box_loss'], label='Val')
plt.title('Box Loss')
plt.legend()

plt.subplot(1, 3, 2)
plt.plot(df['epoch'], df['train/cls_loss'], label='Train')
plt.plot(df['epoch'], df['val/cls_loss'], label='Val')
plt.title('Class Loss')

plt.subplot(1, 3, 3)
plt.plot(df['epoch'], df['train/dfl_loss'], label='Train')
plt.plot(df['epoch'], df['val/dfl_loss'], label='Val')
plt.title('DFL Loss')
plt.show()