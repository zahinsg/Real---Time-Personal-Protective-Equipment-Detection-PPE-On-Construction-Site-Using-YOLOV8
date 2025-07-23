import os
import shutil
import yaml

# === CONFIGURATION ===
original_yaml_path = r'C:/Users/User/Desktop/SEM 6/CSP650/FYP PROJECT/DATASET/sh5.yaml'
source_dataset_path = r'C:/Users/User/Desktop/SEM 6/CSP650/FYP PROJECT/DATASET/newdataset'
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

# === CREATE OUTPUT FOLDERS ===
for class_name in selected_class_names:
    os.makedirs(os.path.join(output_dataset_path, f'separated{class_name}', 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dataset_path, f'separated{class_name}', 'labels'), exist_ok=True)

# Create a dedicated folder for multi-class images
os.makedirs(os.path.join(output_dataset_path, 'multiclass', 'images'), exist_ok=True)
os.makedirs(os.path.join(output_dataset_path, 'multiclass', 'labels'), exist_ok=True)

# === SEPARATION FUNCTION FOR MULTICLASS AND SINGLE CLASS ===
def separate_multiclass():
    label_dir = os.path.join(source_dataset_path, 'labels')
    image_dir = os.path.join(source_dataset_path, 'images')

    total_files = 0
    copied_files = 0
    copied_images = set()

    for label_file in os.listdir(label_dir):
        if not label_file.endswith('.txt'):
            continue

        total_files += 1
        label_path = os.path.join(label_dir, label_file)

        with open(label_path, 'r') as f:
            lines = f.readlines()

        # Track which classes are present in the current file
        class_present = set()

        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            try:
                original_class_id = int(parts[0])
                if original_class_id in class_id_mapping:
                    class_name = class_id_mapping[original_class_id]
                    class_present.add(class_name)
            except ValueError:
                print(f"⚠️ Invalid label format in file {label_file}: {line}")
                continue

        # Determine if the image is multiclass or single class
        if len(class_present) > 1:
            class_folder = 'multiclass'
        else:
            class_folder = f'separated{next(iter(class_present))}' if class_present else 'unknown'

        output_image_dir = os.path.join(output_dataset_path, class_folder, 'images')
        output_label_dir = os.path.join(output_dataset_path, class_folder, 'labels')

        # Copy label file to appropriate folder
        dst_label_path = os.path.join(output_label_dir, label_file)
        shutil.copy(label_path, dst_label_path)

        # Try to copy the corresponding image file
        image_found = False
        for ext in image_extensions:
            image_file = label_file.replace('.txt', ext)
            src_img_path = os.path.join(image_dir, image_file)

            # Avoid duplicates
            if os.path.exists(src_img_path) and src_img_path not in copied_images:
                dst_img_path = os.path.join(output_image_dir, image_file)
                try:
                    shutil.copy(src_img_path, dst_img_path)
                    copied_files += 1
                    copied_images.add(src_img_path)
                    image_found = True
                    print(f'✅ Copied {class_folder}: {src_img_path} to {dst_img_path}')
                    break
                except Exception as e:
                    print(f'❌ Failed to copy {src_img_path}: {e}')
                    continue

        if not image_found:
            print(f'⚠️ Image not found for {label_file}')

    # Summary
    print(f'\n✅ Total Label Files Processed: {total_files}')
    print(f'✅ Total Copied Files: {copied_files}')

# === RUN THE MULTICLASS SEPARATION PROCESS ===
separate_multiclass()

print('\n✅ Images and labels separated by class, including multi-class handling.')
