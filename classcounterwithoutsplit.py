import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# Define class names
CLASS_NAMES = ['face-mask', 'gloves', 'helmet', 'shoes', 'safety-vest']

# Path to labels directory
LABELS_DIR = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\newdataset\labels'  # Update with actual path

# Function to build co-occurrence matrix and count class instances
def build_cooccurrence_matrix(label_dir):
    co_matrix = np.zeros((len(CLASS_NAMES), len(CLASS_NAMES)), dtype=int)
    class_counts = Counter()

    for label_file in os.listdir(label_dir):
        if not label_file.endswith('.txt'):
            continue
        file_path = os.path.join(label_dir, label_file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
        classes_in_image = [int(line.split()[0]) for line in lines]

        # Update co-occurrence counts and count each instance of the class
        for cls1 in classes_in_image:
            class_counts[cls1] += 1
            for cls2 in set(classes_in_image):
                co_matrix[cls1, cls2] += 1

    return co_matrix, class_counts

# Function to plot heatmap
#def plot_heatmap(matrix, title):
#    plt.figure(figsize=(8, 6))
#    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues', xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
#    plt.title(title)
#    plt.xlabel('Class ID')
#    plt.ylabel('Class ID')
#    plt.tight_layout()
#    plt.show()

# Function to plot bar chart
def plot_bar_chart(class_counts):
    plt.figure(figsize=(8, 4))
    ids, counts = zip(*sorted(class_counts.items()))
    plt.bar([CLASS_NAMES[i] for i in ids], counts, color='skyblue')
    for i, count in enumerate(counts):
        plt.text(i, count + 1, str(count), ha='center', va='bottom')
    plt.title('Class Instance Frequency')
    plt.xlabel('Class Name')
    plt.ylabel('Instance Count')
    plt.tight_layout()
    plt.show()

# Main processing
if os.path.exists(LABELS_DIR):
    co_matrix, class_counts = build_cooccurrence_matrix(LABELS_DIR)
#    plot_heatmap(co_matrix, title='Class Co-occurrence Heatmap')
    plot_bar_chart(class_counts)
else:
    print(f'Error: Directory {LABELS_DIR} does not exist.')
