from ultralytics import YOLO

# Load the trained model (best.pt from training)
model = YOLO("IR_model/runs/detect/train/weights/best.pt")

# Make predictions on an image
results = model.predict(source="IR_model/Mahjong_dataset/test/images/17_120_jpg.rf.b883ad531161e057cdf14682ebcc668f.jpg", conf=0.25, save=True)

# Process results
for result in results:
    # Print detected classes and confidence scores
    boxes = result.boxes
    for box in boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = result.names[class_id]
        print(f"Detected: {class_name} (confidence: {confidence:.2f})")
