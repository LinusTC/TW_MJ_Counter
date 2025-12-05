from ultralytics import YOLO


class TileClassifierTFL:

	def __init__(self, image_source, model_path="IR_model/m_model_v2_TFL/best_float32.tflite", conf=0.5):
		self.image_source = image_source
		self.model_path = model_path
		self.conf_threshold = conf
		self.classified_decks = []
		self._model = YOLO(self.model_path)

	def _predict(self, stream=False):
		return self._model.predict(
			source=self.image_source,
			conf=self.conf_threshold,
			stream=stream,
			save=True,
		)

	def classify_photo(self):
		predictions = self._predict(stream=False)
		for result in predictions:
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
		predictions = self._predict(stream=True)

		previous_detection = None
		stable_count = 0
		stability_threshold = 20

		for result in predictions:
			boxes = result.boxes
			detected_tiles = {}

			for box in boxes:
				class_id = int(box.cls[0])
				confidence = float(box.conf[0])
				class_name = result.names[class_id]
				detected_tiles[class_name] = detected_tiles.get(class_name, 0) + 1
				print(f"Detected: {class_name} (confidence: {confidence:.2f})")

			if detected_tiles == previous_detection:
				stable_count += 1
				if stable_count == stability_threshold and detected_tiles:
					self.classified_decks.append(detected_tiles)
			else:
				stable_count = 0
				previous_detection = detected_tiles.copy() if detected_tiles else None

	def get_classified_decks(self):
		return self.classified_decks
