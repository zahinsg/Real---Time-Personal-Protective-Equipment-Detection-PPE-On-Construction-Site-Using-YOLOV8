import os
import glob

#0: face - mask
#1: gloves
#2: helmet
#3: shoes
#4: safety - vest
#5: safety - harness
#6: human
# --- USER CONFIG ---
dataset_path = r"/DATASET/new_filtered_dataset"
label_dir = os.path.join(dataset_path, r"splittedataset\labels\test")

# Initialize a counter for each class (assuming 7 classes, modify this if more/less classes exist)
class_counter = {i: 0 for i in range(7)}  # Assuming there are 7 classes (0-6)

# --- FUNCTION TO COUNT CLASS OCCURRENCES ---

def count_classes_in_labels(label_path):
    """Read the label file and update the class counter based on the first column."""
    with open(label_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split()
        if parts:
            class_id = int(parts[0])  # First column is the class ID
            if class_id in class_counter:
                class_counter[class_id] += 1

# --- MAIN SCRIPT ---

def main():
    label_files = glob.glob(label_dir + "/*.txt")  # Get all label files

    # Process each label file
    for label_file in label_files:
        count_classes_in_labels(label_file)

    # Print the class counts
    print("Class distribution:")
    for class_id, count in class_counter.items():
        print(f"Class {class_id}: {count} occurrences")

if __name__ == "__main__":
    main()
#BEFORE AUGMENT
#Class 0: 670 occurrences
#Class 1: 2790 occurrences
#Class 2: 927 occurrences
#Class 3: 4560 occurrences
#Class 4: 5024 occurrences
#Class 5: 2164 occurrences
#Class 6: 1545 occurrences

#AFTER AUGMENT
#Class 0: 3030 occurrences
#Class 1: 2790 occurrences
#Class 2: 4635 occurrences
#Class 3: 4560 occurrences
#Class 4: 5024 occurrences
#Class 5: 2164 occurrences
#Class 6: 7725 occurrences

#SPLITTED DATASET (0.7:0.2:0.1)
#train
#Class 0: 2084 occurrences
#Class 1: 1953 occurrences
#Class 2: 3213 occurrences
#Class 3: 3168 occurrences
#Class 4: 3431 occurrences
#Class 5: 1556 occurrences
#Class 6: 5464 occurrences

#val
#Class 0: 623 occurrences
#Class 1: 576 occurrences
#Class 2: 931 occurrences
#Class 3: 917 occurrences
#Class 4: 1079 occurrences
#Class 5: 376 occurrences
#Class 6: 1512 occurrences

#test
#Class 0: 323 occurrences
#Class 1: 261 occurrences
#Class 2: 491 occurrences
#Class 3: 475 occurrences
#Class 4: 514 occurrences
#Class 5: 232 occurrences
#Class 6: 749 occurrences

