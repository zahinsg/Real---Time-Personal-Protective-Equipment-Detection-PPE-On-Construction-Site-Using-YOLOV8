#S1 verify whether images and label are the same with each other, if they do not correlate then remove
#S2 filter the class that you want, only keep the images that have the desired class label
#S3 change original class ID to desired class ID,
#S4 count the instances of each class if

#dataset imbalance
#S5 find new data to add on
#S6 data augmentation (apply the agmentoneclass.py)
#S7 check for imbalance

#run your experiment
#=========================S 1=======================================================================================
import os
from tqdm import tqdm

# Directories for images and labels
image_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\backup\archive (12)\archive (12)\images'
label_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\backup\archive (12)\archive (12)\labels'

# Supported image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
label_extensions = ['.txt', '.xml']

# Get lists of file names without extensions
image_files = {os.path.splitext(f)[0] for f in os.listdir(image_dir) if os.path.splitext(f)[1].lower() in image_extensions}
label_files = {os.path.splitext(f)[0] for f in os.listdir(label_dir) if os.path.splitext(f)[1].lower() in label_extensions}

# Find unmatched files
unmatched_images = image_files - label_files
unmatched_labels = label_files - image_files

print(f'Total unmatched images: {len(unmatched_images)}')
print(f'Total unmatched labels: {len(unmatched_labels)}')

# Delete unmatched images with progress bar
for img in tqdm(unmatched_images, desc='Removing unmatched images'):
    for ext in image_extensions:
        img_path = os.path.join(image_dir, img + ext)
        if os.path.exists(img_path):
            os.remove(img_path)

# Delete unmatched labels with progress bar
for lbl in tqdm(unmatched_labels, desc='Removing unmatched labels'):
    for ext in label_extensions:
        lbl_path = os.path.join(label_dir, lbl + ext)
        if os.path.exists(lbl_path):
            os.remove(lbl_path)

print('Filtering completed.')
