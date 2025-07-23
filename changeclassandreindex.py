import os
import shutil
import yaml
#this is for no split data
# === CONFIGURATION ===
original_yaml_path = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\sh17.yaml'
source_dataset_path = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\backup\archive (14)'
output_dataset_path = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\revisedataset'

selected_class_names = ['face-mask', 'gloves', 'helmet', 'shoes', 'safety-vest']

# Supported image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.xml']

# === LOAD ORIGINAL CLASS NAMES ===
with open(original_yaml_path, 'r') as f:
    data = yaml.safe_load(f)

all_classes = data['names']

# Correct class ID mapping
class_id_mapping = {
    5: 0,   # face-mask
    9: 1,   # gloves
    10: 2,  # helmet
    14: 3,  # shoes
    16: 4   # safety-vest
}

print('🎯 Class ID Mapping:', class_id_mapping)

# === CREATE OUTPUT FOLDERS ===
os.makedirs(os.path.join(output_dataset_path, 'images'), exist_ok=True)
os.makedirs(os.path.join(output_dataset_path, 'labels'), exist_ok=True)

# === FILTERING FUNCTION ===
def process_files():
    label_dir = os.path.join(source_dataset_path, 'labels')
    image_dir = os.path.join(source_dataset_path, 'images')
    output_label_dir = os.path.join(output_dataset_path, 'labels')
    output_image_dir = os.path.join(output_dataset_path, 'images')

    copied_count = 0
    skipped_count = 0
    missing_images = 0
    total = 0

    for label_file in os.listdir(label_dir):
        if not label_file.endswith('.txt'):
            continue

        total += 1
        label_path = os.path.join(label_dir, label_file)

        with open(label_path, 'r') as f:
            lines = f.readlines()

        filtered_lines = []
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            try:
                # Ensure the class ID is an integer
                original_class_id = int(parts[0])
                # Check if the class ID is in the remapping dictionary
                if original_class_id in class_id_mapping:
                    new_class_id = class_id_mapping[original_class_id]
                    # Form the new line with the mapped class ID and original coordinates
                    new_line = f'{new_class_id} ' + ' '.join(parts[1:]) + '\n'
                    filtered_lines.append(new_line)
            except ValueError:
                print(f"Invalid label format in file {label_file}: {line}")
                continue


        if filtered_lines:
            # Try all common extensions
            image_found = False
            for ext in image_extensions:
                image_file = label_file.replace('.txt', ext)
                src_img_path = os.path.join(image_dir, image_file)
                if os.path.exists(src_img_path):
                    dst_img_path = os.path.join(output_image_dir, image_file)
                    shutil.copy(src_img_path, dst_img_path)
                    image_found = True
                    break

            if image_found:
                dst_label_path = os.path.join(output_label_dir, label_file)
                with open(dst_label_path, 'w') as f:
                    f.writelines(filtered_lines)
                copied_count += 1
            else:
                print(f'⚠️ Image not found for {label_file}')
                missing_images += 1
        else:
            skipped_count += 1
            print(f'⏭️ Skipped: {label_file} (no matching class)')

    # Summary
    print(f'\n📂 Summary')
    print(f'🔢 Total label files: {total}')
    print(f'✅ Copied (with desired classes): {copied_count}')
    print(f'⏭️ Skipped (no matching classes): {skipped_count}')
    print(f'❌ Missing images: {missing_images}')

# === RUN THE PROCESS ===
process_files()

# === WRITE NEW YAML FILE ===
new_yaml = {
    'train': os.path.abspath(os.path.join(output_dataset_path, 'images')),
    'val': os.path.abspath(os.path.join(output_dataset_path, 'images')),  # Modify as needed
    'test': os.path.abspath(os.path.join(output_dataset_path, 'images')),  # Modify as needed
    'names': selected_class_names,
    'nc': len(selected_class_names)
}

yaml_path = os.path.join(output_dataset_path, 'sh5.yaml')
with open(yaml_path, 'w') as f:
    yaml.dump(new_yaml, f)

print('\n✅ Done! Filtered dataset saved to:', output_dataset_path)
print('📝 New YAML file:', yaml_path)
