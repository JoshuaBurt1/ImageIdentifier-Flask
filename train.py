from ultralytics import YOLO

model = YOLO('yolov8n-cls.pt')  # load a pretrained model (recommended for training)

model.train(data='C:/Users/Josh/Desktop/WebDev/Python/imageIdentifiers/mushroom_dataset', epochs=20, imgsz=64)

#yolo classify train data='C:/Users/Josh/Desktop/WebDev/Python/imageIdentifiers/mushroom_dataset' model=yolov8n-cls.pt  epochs=1 imgsz=64
