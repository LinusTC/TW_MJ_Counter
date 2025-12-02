from ultralytics import YOLO

class TileClassifier:
    def __init__(self, image_url):
        self.image_url = image_url
        self.classified_decks = []        

    def classify(self):
        pretrained_model = YOLO("IR_model/runs/detect/m_model_v2/weights/last.pt")
        all_results = pretrained_model.predict(source=self.image_url, conf=0.5, save=True)

        for result in all_results:
            boxes = result.boxes
            detected_tiles = {}

            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = result.names[class_id]
                detected_tiles[class_name] = detected_tiles.get(class_name, 0) + 1
                print(f"Detected: {class_name} (confidence: {confidence:.2f})")

            self.classified_decks.append(detected_tiles)
    
    def get_classified_decks(self):
        return self.classified_decks