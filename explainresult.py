from ultralytics import YOLO

def main():
    # Path to your model and dataset YAML file
    model_path = r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train2\weights\best.pt"
    data_path = r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\sh5.yaml"

    # Load the model
    model = YOLO(model_path)

    # Run the validation
    results = model.val(data=data_path)

    # Print the results (mAP and per-class performance)
    print(results)

if __name__ == "__main__":
    main()
