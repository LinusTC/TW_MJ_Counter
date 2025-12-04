from ultralytics import YOLO

class TileClassifier:
    def __init__(self, image_source):
        self.image_source = image_source
        self.classified_decks = []        

    def classify_photo(self):
        pretrained_model = YOLO("IR_model/runs/detect/m_model_v2/weights/best.pt")
        all_results = pretrained_model.predict(source=self.image_source, conf=0.5, save=True)

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

    def classify_video(self):
        pretrained_model = YOLO("IR_model/runs/detect/m_model_v2/weights/best.pt")
        all_results = pretrained_model.predict(source=self.image_source, conf=0.5, stream=True, save = True)

        previous_detection = None
        stable_count = 0
        stability_threshold = 20
        
        for result in all_results:
            boxes = result.boxes
            detected_tiles = {}

            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = result.names[class_id]
                detected_tiles[class_name] = detected_tiles.get(class_name, 0) + 1
                print(f"Detected: {class_name} (confidence: {confidence:.2f})")

            # Check if current detection matches previous one
            if detected_tiles == previous_detection:
                stable_count += 1
                # Once we reach stability threshold, save it (only once)
                if stable_count == stability_threshold and detected_tiles:
                    self.classified_decks.append(detected_tiles)
            else:
                stable_count = 0
                previous_detection = detected_tiles.copy() if detected_tiles else None
    
    def get_classified_decks(self):
        return self.classified_decks