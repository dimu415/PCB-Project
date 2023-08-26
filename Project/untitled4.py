import ultralytics
from ultralytics import YOLO
model=YOLO('yolov8n.pt')
model.train(data='C:/Users/USER/Desktop/img2/data.yaml',epochs=100,patience=30,batch=32,imgsz=416)