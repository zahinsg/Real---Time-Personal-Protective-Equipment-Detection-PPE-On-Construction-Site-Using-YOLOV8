import os
import matplotlib.pyplot as plt
from collections import defaultdict

# === CONFIGURATION ===
base_path = r'C:/Users/User/Desktop/SEM 6/CSP650/FYP PROJECT/DATASET/revisedataset'
subfolders = ['multi_class', 'separatedface-mask', 'separatedgloves',
              'separatedhelmet', 'separatedsafety-vest', 'separatedshoes']

# Class names corresponding to your setup (including multi-class)
class_names = ['face-mask', 'gloves', 'helmet', 'shoes', 'safety-vest', 'multi_class']

# Dictionary to count the number of images per class
class_counts = defaultdict(int)

# === READ LABELS AND COUNT IMAGES ===
for subfolder in subfolders:
    label_path = os.path.join(base_path, subfolder, 'labels')
    if not os.path.exists(label_path):
        print(f"⚠️ Labels folder not found in {subfolder}. Skipping.")
        continue

    image_count = 0

    for label_file in os.listdir(label_path):
        if label_file.endswith('.txt'):
            image_count += 1

    # Map the subfolder to the class name
    if subfolder == 'multi_class':
        class_counts['multi_class'] = image_count
    else:
        # Extract the class name from the subfolder name
        for class_name in class_names:
            if class_name in subfolder:
                class_counts[class_name] = image_count

# === PLOT THE GRAPH ===
plt.figure(figsize=(8, 5))
bars = plt.bar(class_counts.keys(), class_counts.values(), color='skyblue')

# Add exact numbers on top of each bar
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval, str(yval),
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.xlabel('Class Names')
plt.ylabel('Number of Images')
plt.title('Image Distribution Across Classes (Including Multi-Class)')
plt.xticks(rotation=45)
plt.tight_layout()

# Display the bar plot
plt.show()
