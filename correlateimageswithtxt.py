from pathlib import Path
import shutil

# === CONFIGURATION ===
txt_folder = Path(r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\Safety Vests.v1-raw-images.yolov8\train\new labels")  # Folder containing .txt annotation files
img_folder = Path(r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\Safety Vests.v1-raw-images.yolov8\train\images")  # Folder containing all original images
output_folder = Path(r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\Safety Vests.v1-raw-images.yolov8\filtered_images")  # Folder to copy matching images to

# === Create output folder if it doesn't exist ===
output_folder.mkdir(parents=True, exist_ok=True)

# === Image extensions to check ===
image_extensions = [".jpg", ".jpeg", ".png"]

# === Copy matching images and delete non-matching files ===
copied = 0
deleted = 0
for txt_file in txt_folder.glob("*.txt"):
    base_name = txt_file.stem
    print(f"Processing: {txt_file.name}...")  # Debugging line to see which txt file is being processed

    # Check if image exists for the current .txt file
    image_found = False
    for ext in image_extensions:
        image_path = img_folder / f"{base_name}{ext}"
        if image_path.exists():
            print(f"Found image: {image_path.name}")  # Debugging line to confirm image exists
            shutil.copy2(image_path, output_folder / image_path.name)
            copied += 1
            image_found = True
            break  # Stop checking once a match is found

    # If no matching image was found, delete the txt file
    if not image_found:
        print(f"Image for {txt_file.name} not found. Deleting txt file.")
        txt_file.unlink()  # Delete the .txt file
        deleted += 1

# Check for any images that have no corresponding .txt file and delete them
for img_file in img_folder.glob("*"):
    if img_file.suffix.lower() in image_extensions:
        base_name = img_file.stem
        txt_file = txt_folder / f"{base_name}.txt"
        if not txt_file.exists():  # If no matching .txt file exists
            print(f"No txt file for image: {img_file.name}. Deleting image.")
            img_file.unlink()  # Delete the image
            deleted += 1

print(f"\n✅ {copied} images copied to: {output_folder}")
print(f"❌ {deleted} files (images or txt) were deleted due to no matching pair.")
