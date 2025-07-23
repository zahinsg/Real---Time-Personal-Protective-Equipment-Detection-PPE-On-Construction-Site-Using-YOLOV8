import os
from collections import defaultdict
import matplotlib.pyplot as plt

# === CONFIGURATION ===
label_dir = r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\newlabels"

# Class ID to Name Mapping (Update as per your classes)
class_id_to_name = {
    0: 'face-mask',
    1: 'gloves',
    2: 'helmet',
    3: 'shoes',
    4: 'safety-vest'
}

# Initialize counters for images per class
image_count_per_class = defaultdict(set)  # Use a set to avoid duplicates
multi_class_count = 0
total_images = 0

# === PROCESSING IMAGES ===
for label_file in os.listdir(label_dir):
    if not label_file.endswith('.txt'):
        continue

    label_path = os.path.join(label_dir, label_file)
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()

        # Use a set to track unique classes in this image
        unique_classes = set()

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            try:
                class_id = int(parts[0])
                unique_classes.add(class_id)
            except ValueError:
                print(f"Invalid label format in file {label_file}: {line}")
                continue

        # Update the count for each unique class found in the image
        for cls_id in unique_classes:
            image_count_per_class[cls_id].add(label_file)

        # Check if the image has multiple classes
        if len(unique_classes) > 1:
            multi_class_count += 1

        # Update the total image count
        total_images += 1

    except Exception as e:
        print(f"Error processing file {label_file}: {e}")

# === PRINT SUMMARY ===
print("\n📊 Unique Image Count per Class:")
for class_id, images in sorted(image_count_per_class.items()):
    class_name = class_id_to_name.get(class_id, f'Unknown ({class_id})')
    print(f"📝 Class '{class_name}' (ID {class_id}): {len(images)} unique images")

print(f"\n🌟 Total Images Processed: {total_images}")
print(f"🔄 Multi-Class Images (contain more than one class): {multi_class_count}")

# === PLOT BAR CHART ===
def plot_image_count_bar(image_count):
    plt.figure(figsize=(8, 5))
    class_names = [class_id_to_name.get(class_id, f'Class {class_id}') for class_id in sorted(image_count.keys())]
    counts = [len(image_count[class_id]) for class_id in sorted(image_count.keys())]

    # Create the bar plot
    bars = plt.bar(class_names, counts, color='skyblue')

    # Add exact number of images on top of each bar
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 5, f'{count}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xlabel('Class Name')
    plt.ylabel('Number of Instances')
    plt.title('Number of Instances per Class')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plot the unique image count per class
plot_image_count_bar(image_count_per_class)
