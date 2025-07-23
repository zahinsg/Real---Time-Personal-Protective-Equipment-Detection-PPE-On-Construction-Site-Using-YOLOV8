import os
import shutil
import yaml

# === CONFIGURATION ===
original_yaml_path = r'/DATASET/backup/safetyvestsafetyharnesshelmetadditional/data.yaml'
source_dataset_path = r'/DATASET/backup/safetyvestsafetyharnesshelmetadditional'
output_dataset_path = r'/DATASET/additionalHHV'

selected_class_names = ['Mask']
image_extensions = ['.jpg', '.jpeg', '.png']

# === LOAD ORIGINAL CLASS NAMES ===
with open(original_yaml_path, 'r') as f:
    data = yaml.safe_load(f)

all_classes = data['names']
mask_id = next((i for i, name in enumerate(all_classes) if name == 'Mask'), None)
print('🎯 Mask Class ID:', mask_id)

if mask_id is None:
    print('Error: Mask class not found in YAML file.')
    exit(1)

# === CREATE OUTPUT FOLDERS ===
os.makedirs(os.path.join(output_dataset_path, 'images'), exist_ok=True)
os.makedirs(os.path.join(output_dataset_path, 'labels'), exist_ok=True)

# === PROCESSING FILES ===
copied_count = 0
skipped_count = 0
missing_images = 0

label_dir = os.path.join(source_dataset_path, 'labels')
image_dir = os.path.join(source_dataset_path, 'images')
output_label_dir = os.path.join(output_dataset_path, 'labels')
output_image_dir = os.path.join(output_dataset_path, 'images')

for label_file in os.listdir(label_dir):
    if not label_file.endswith('.txt'):
        continue

    label_path = os.path.join(label_dir, label_file)
    with open(label_path, 'r') as f:
        lines = f.readlines()

    filtered_lines = []
    for line in lines:
        parts = line.strip().split()
        if parts and int(parts[0]) == mask_id:
            filtered_lines.append(line)

    if filtered_lines:
        base_name = os.path.splitext(label_file)[0]
        image_found = False
        for ext in image_extensions:
            img_path = os.path.join(image_dir, base_name + ext)
            if os.path.exists(img_path):
                shutil.copy(img_path, os.path.join(output_image_dir, base_name + ext))
                with open(os.path.join(output_label_dir, label_file), 'w') as f:
                    f.writelines(filtered_lines)
                copied_count += 1
                image_found = True
                break
        if not image_found:
            missing_images += 1
    else:
        skipped_count += 1

print(f'✅ Copied: {copied_count}, ⏭️ Skipped: {skipped_count}, ❌ Missing Images: {missing_images}')

# === WRITE NEW YAML FILE ===
new_yaml = {
    'train': os.path.abspath(os.path.join(output_dataset_path, 'images')),
    'names': ['Mask'],
    'nc': 1
}

yaml_path = os.path.join(output_dataset_path, 'mask.yaml')
with open(yaml_path, 'w') as f:
    yaml.dump(new_yaml, f)

print('✅ Done! Filtered dataset and YAML saved to:', output_dataset_path)


