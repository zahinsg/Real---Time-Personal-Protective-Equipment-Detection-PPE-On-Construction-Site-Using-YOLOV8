import os
import cv2
from tqdm import tqdm

# Configuration
image_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\images'
label_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\labels'
output_dir = r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\separated_classes\multiclass\augmented\visualized'

# Face-mask class only
class_id = 0
class_name = 'face-mask'
color = (0, 255, 0)  # Green bounding box

def create_output_dir():
    """Create output directory for visualized images."""
    os.makedirs(output_dir, exist_ok=True)

def load_yolo_labels(label_path):
    """Load YOLO format labels."""
    with open(label_path, 'r') as f:
        lines = f.readlines()
    bboxes = [list(map(float, line.strip().split())) for line in lines]
    return bboxes

def draw_bounding_box(image, bbox, label):
    """Draw a bounding box with a label."""
    x_center, y_center, width, height = bbox
    img_height, img_width = image.shape[:2]

    # Convert normalized coordinates to pixel values
    x_min = int((x_center - width / 2) * img_width)
    y_min = int((y_center - height / 2) * img_height)
    x_max = int((x_center + width / 2) * img_width)
    y_max = int((y_center + height / 2) * img_height)

    # Draw rectangle
    cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

    # Draw label
    cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def visualize_bounding_boxes(image_path, label_path):
    """Visualize bounding boxes on an image."""
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image {image_path}")
        return None

    bboxes = load_yolo_labels(label_path)
    for bbox in bboxes:
        # Check if the bbox corresponds to the face-mask class
        if int(bbox[0]) == class_id:
            draw_bounding_box(image, bbox[1:], class_name)

    return image

def visualize_face_mask():
    """Visualize bounding boxes for all face-mask images."""
    create_output_dir()

    for file in tqdm(os.listdir(label_dir)):
        if not file.endswith('.txt'):
            continue

        img_name = os.path.splitext(file)[0]
        label_path = os.path.join(label_dir, file)

        # Check for multiple extensions
        possible_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_path = None
        for ext in possible_extensions:
            potential_path = os.path.join(image_dir, img_name + ext)
            if os.path.exists(potential_path):
                image_path = potential_path
                break

        if image_path is None:
            print(f"Image not found for label: {label_path}")
            continue

        # Visualize bounding boxes
        visualized_image = visualize_bounding_boxes(image_path, label_path)

        if visualized_image is not None:
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            cv2.imwrite(output_path, visualized_image)
            print(f"Saved visualized image: {output_path}")

    print("Visualization complete.")

# Run the visualization process
if __name__ == "__main__":
    visualize_face_mask()
