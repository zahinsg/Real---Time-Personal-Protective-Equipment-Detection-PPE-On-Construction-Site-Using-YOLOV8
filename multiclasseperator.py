import os
import shutil
import yaml

# === CONFIGURATION ===
original_yaml_path = r'C:/Users/User/Desktop/SEM 6/CSP650/FYP PROJECT/DATASET/sh5.yaml'
multiclass_path = r'C:/Users/User/Desktop/SEM 6/CSP650/FYP PROJECT/DATASET/separated_classes/multiclass'
output_dataset_path = r'C:/Users/User/Desktop/SEM 6/CSP650/FYP PROJECT/DATASET/separated_classes'

# Desired class names
selected_class_names = ['face-mask', 'gloves', 'helmet', 'shoes', 'safety-vest']
image_extensions = ['.png', '.jpg', '.jpeg']

# === LOAD ORIGINAL CLASS NAMES ===
with open(original_yaml_path, 'r') as f:
    data = yaml.safe_load(f)
all_classes = data['names']

# Create a dictionary to map original class IDs to desired class names
class_id_mapping = {i: name for i, name in all_classes.items() if name in selected_class_names}
print('🎯 Class ID Mapping:', class_id_mapping)

# === FUNCTION TO SEPARATE MULTI-CLASS COMBINATIONS ===
def separate_combinations():
    label_dir = os.path.join(multiclass_path, 'labels')
    image_dir = os.path.join(multiclass_path, 'images')
    copied_images = set()

    for label_file in os.listdir(label_dir):
        if not label_file.endswith('.txt'):
            continue

        label_path = os.path.join(label_dir, label_file)
        with open(label_path, 'r') as f:
            lines = f.readlines()

        class_present = set()
        for line in lines:
            parts = line.strip().split()
            if len(parts) > 0:
                try:
                    class_id = int(parts[0])
                    if class_id in class_id_mapping:
                        class_present.add(class_id_mapping[class_id])
                except ValueError:
                    print(f'⚠️ Invalid format in {label_file}: {line}')

        # Create a folder name based on class combination
        combination_name = "_".join(sorted(class_present))
        combination_folder = os.path.join(output_dataset_path, f'multiclass_{combination_name}')
        os.makedirs(os.path.join(combination_folder, 'images'), exist_ok=True)
        os.makedirs(os.path.join(combination_folder, 'labels'), exist_ok=True)

        # Copy label file
        dst_label_path = os.path.join(combination_folder, 'labels', label_file)
        shutil.copy(label_path, dst_label_path)

        # Copy the corresponding image without duplication
        for ext in image_extensions:
            image_file = label_file.replace('.txt', ext)
            src_img_path = os.path.join(image_dir, image_file)

            # Check for duplicates with combination
            if os.path.exists(src_img_path) and (combination_name, src_img_path) not in copied_images:
                dst_img_path = os.path.join(combination_folder, 'images', image_file)
                try:
                    shutil.copy(src_img_path, dst_img_path)
                    copied_images.add((combination_name, src_img_path))
                    print(f'✅ Copied: {src_img_path} to {dst_img_path}')
                    break
                except Exception as e:
                    print(f'❌ Error copying {src_img_path}: {e}')

    print('\n✅ Combination separation completed successfully.')

# === RUN SEPARATION ===
separate_combinations()
