import os
import random
import shutil

# Set seed for reproducibility
SEED = 50
#before augment seed= 50
#after augment seed=40
random.seed(SEED)

# Configuration
input_image_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\newdataset\images'
input_label_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\newdataset\labels'
output_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\splittedbeforeaugment'
train_ratio = 0.8  # 80% training, 20% validation


def create_output_dirs():
    """Create train and val directories for images and labels."""
    os.makedirs(os.path.join(output_dir, 'train', 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'train', 'labels'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'val', 'images'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'val', 'labels'), exist_ok=True)

def get_image_label_pairs():
    """Get a list of image and label pairs."""
    image_files = [f for f in os.listdir(input_image_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
    image_label_pairs = []

    for image_file in image_files:
        base_name = os.path.splitext(image_file)[0]
        label_file = base_name + '.txt'
        label_path = os.path.join(input_label_dir, label_file)

        if os.path.exists(label_path):
            image_label_pairs.append((image_file, label_file))

    return image_label_pairs

def split_dataset(image_label_pairs):
    """Split the dataset into training and validation sets."""
    random.shuffle(image_label_pairs)
    split_point = int(len(image_label_pairs) * train_ratio)

    train_pairs = image_label_pairs[:split_point]
    val_pairs = image_label_pairs[split_point:]

    return train_pairs, val_pairs

def copy_files(pairs, subset):
    """Copy image-label pairs to the respective train or val directory."""
    for image_file, label_file in pairs:
        # Paths for images
        src_image_path = os.path.join(input_image_dir, image_file)
        dst_image_path = os.path.join(output_dir, subset, 'images', image_file)

        # Paths for labels
        src_label_path = os.path.join(input_label_dir, label_file)
        dst_label_path = os.path.join(output_dir, subset, 'labels', label_file)

        # Copy files
        shutil.copy(src_image_path, dst_image_path)
        shutil.copy(src_label_path, dst_label_path)
        print(f"Copied {image_file} and {label_file} to {subset} set.")

def main():
    """Main function to split the dataset."""
    create_output_dirs()
    image_label_pairs = get_image_label_pairs()
    train_pairs, val_pairs = split_dataset(image_label_pairs)

    # Copy to train and val directories
    copy_files(train_pairs, 'train')
    copy_files(val_pairs, 'val')

    print(f"Dataset split completed: {len(train_pairs)} train, {len(val_pairs)} val")

if __name__ == "__main__":
    main()
