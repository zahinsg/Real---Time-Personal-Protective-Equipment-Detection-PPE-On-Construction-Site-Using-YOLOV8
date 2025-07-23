from sympy import false
from ultralytics import YOLO

if __name__ =='__main__':
    # Load the model architecture
    model = YOLO(r'C:\Users\User\Desktop\SEM 6\CSP650\FYP PROJECT\DATASET\runs\detect\train17\weights\last.pt')

    # Train the model on your custom dataset
    model.train(data="sh6.yaml", epochs=100, imgsz=640, resume=True)

#learning rate
#optimizer
#epochs 50/100
#batch size 
#before and after augmented
#optional
#test on new model

#kena resume training 14