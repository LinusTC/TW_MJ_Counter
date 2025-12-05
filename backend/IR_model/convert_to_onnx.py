from ultralytics import YOLO

model = YOLO("runs/detect/m_model_v2/weights/best.pt")

model.export(format="onnx", optimize=True)