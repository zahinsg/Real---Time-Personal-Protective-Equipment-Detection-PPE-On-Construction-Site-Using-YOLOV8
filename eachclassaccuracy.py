from ultralytics import YOLO
if __name__ =='__main__':

# Load trained model
    model = YOLO(r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train16\weights\last.pt')
# Run validation again to regenerate per-class stats
    metrics = model.val(data=r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\sh6.yaml')

