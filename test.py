from ultralytics import YOLO

# Load the trained model
model = YOLO(r"C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train2\weights\best.pt")

# Run inference
results = model(r"C:\Users\User\Downloads\0_ojc0v8la1o5iR4NI.jpg")

# Display the results
results[0].show()

# Save the image with bounding boxes to Downloads
#results[0].save(filename=r"C:\Users\User\Downloads")
