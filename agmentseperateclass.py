import os
import random
import cv2
import numpy as np
import hashlib
from itertools import combinations
from albumentations import (
    HorizontalFlip, VerticalFlip, Rotate, RandomBrightnessContrast,
    HueSaturationValue, GaussianBlur, RandomGamma, Compose
)
from tqdm import tqdm

# Set seed for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
cv2.setRNGSeed(SEED)

# Configuration
input_image_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\separatedsafety-vest\images'
input_label_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\separatedsafety-vest\labels'
output_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\separatedsafety-vest\augmented'
target_count = 1287  # Target number of images
class_id = 4  # Face-mask class ID

# Track hashes of augmented images to detect duplicates
image_hashes = set()



# Augmentation Definitions
AUGMENTATIONS = [
    HorizontalFlip(p=1),
    VerticalFlip(p=1),
    Rotate(limit=random.randint(20, 45), p=1),  # Randomize rotation limit
    RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=1),  # Vary brightness/contrast
    HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=1),  # Vary HSV
    GaussianBlur(blur_limit=(3, 7), p=1),  # Vary blur kernel size
    RandomGamma(gamma_limit=(80, 120), p=1)  # Add gamma variation
]

def generate_combinations():
    """Generate all non-empty unique combinations of augmentations."""
    all_combinations = []
    for r in range(1, len(AUGMENTATIONS) + 1):
        comb = list(combinations(AUGMENTATIONS, r))
        all_combinations.extend(comb)
    random.shuffle(all_combinations)
    return all_combinations

def create_augmentation_pipeline(selected_augmentations):
    """Creates a specific augmentation pipeline."""
    return Compose(list(selected_augmentations), bbox_params={'format': 'yolo', 'label_fields': ['category_ids']})

def find_image_path(img_name):
    """Find the image path with various possible extensions."""
    possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    for ext in possible_extensions:
        image_path = os.path.join(input_image_dir, img_name + ext)
        if os.path.exists(image_path):
            return image_path
    print(f"Image not found for: {img_name}")
    return None

def load_yolo_labels(label_path):
    """Load YOLO format labels."""
    try:
        with open(label_path, 'r') as f:
            lines = f.readlines()
        bboxes = [list(map(float, line.strip().split())) for line in lines]
        return bboxes
    except Exception as e:
        print(f"Error loading labels from {label_path}: {e}")
        return []

def calculate_combination_hash(image, combination):
    """Calculate a unique hash for the given image and augmentation combination."""
    image_hash = hashlib.md5(image.tobytes()).hexdigest()
    combination_hash = hashlib.md5(str(combination).encode()).hexdigest()
    return image_hash + combination_hash

def save_yolo_labels(label_path, bboxes):
    """Save YOLO format labels."""
    with open(label_path, 'w') as f:
        for bbox in bboxes:
            line = ' '.join(map(str, bbox))
            f.write(f"{line}\n")

def save_augmented(image, bboxes, img_name, count, combination):
    """Save augmented image and labels."""
    aug_image_name = f"{img_name}_aug_{count}.jpg"
    aug_label_name = f"{img_name}_aug_{count}.txt"

    # Calculate combined hash (image + transformation)
    combined_hash = calculate_combination_hash(image, combination)
    if combined_hash in image_hashes:
        print(f"Duplicate combination found: {aug_image_name} - Skipping save")
        return False

    cv2.imwrite(os.path.join(output_dir, 'images', aug_image_name), image)
    save_yolo_labels(os.path.join(output_dir, 'labels', aug_label_name), bboxes)
    image_hashes.add(combined_hash)
    print(f"Augmented image saved: {aug_image_name}")
    return True

def process_images():
    """Main function to process and augment images."""
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'labels'), exist_ok=True)

    all_combinations = generate_combinations()
    class_count = 0

    for file in tqdm(os.listdir(input_label_dir)):
        if not file.endswith('.txt'):
            continue

        img_name = os.path.splitext(file)[0]
        image_path = find_image_path(img_name)
        if not image_path:
            continue

        image = cv2.imread(image_path)
        if image is None:
            continue

        label_path = os.path.join(input_label_dir, file)
        bboxes = load_yolo_labels(label_path)

        unique_classes = set(bbox[0] for bbox in bboxes)
        if len(unique_classes) == 1 and list(unique_classes)[0] == class_id:
            save_augmented(image, bboxes, img_name, class_count, combination="original")
            class_count += 1

            combination_index = 0
            while class_count < target_count:
                if combination_index >= len(all_combinations):
                    combination_index = 0  # Restart combinations if exhausted

                combination = all_combinations[combination_index]
                combination_index += 1

                aug_pipeline = create_augmentation_pipeline(combination)
                try:
                    transformed = aug_pipeline(image=image, bboxes=[bbox[1:] for bbox in bboxes],
                                               category_ids=[int(bbox[0]) for bbox in bboxes])
                    aug_image, aug_bboxes = transformed['image'], [
                        [category] + bbox for bbox, category in zip(transformed['bboxes'], transformed['category_ids'])
                    ]
                    if save_augmented(aug_image, aug_bboxes, img_name, class_count, combination):
                        class_count += 1
                except Exception:
                    continue

    print(f"Augmentation completed. Data saved in {output_dir}.")

# Run the augmentation process
if __name__ == "__main__":
    process_images()
