from ultralytics import YOLO

model = YOLO("IR_model/yolo11m.pt")
model.train(data="IR_model/Mahjong_dataset/data.yaml", imgsz=640, batch=8, epochs=100, workers=1, device=0)