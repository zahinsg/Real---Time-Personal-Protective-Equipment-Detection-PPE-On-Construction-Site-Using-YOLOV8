import os
import matplotlib.pyplot as plt

# Paths to image directories
train_img_dir = r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\splitted\train\images"
val_img_dir = r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\splitted\val\images"

# Count image files (common formats)
def count_images(folder):
    return len([f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))])

# Count
train_count = count_images(train_img_dir)
val_count = count_images(val_img_dir)

# Plot
counts = [train_count, val_count]
splits = ['Train', 'Validation']

plt.figure(figsize=(6, 4))
bars = plt.bar(splits, counts, color=['skyblue', 'lightgreen'])
plt.title('Number of Images in Train and Validation Splits')
plt.ylabel('Image Count')
plt.grid(axis='y')

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, height + 5, f'{height}', ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.show()
