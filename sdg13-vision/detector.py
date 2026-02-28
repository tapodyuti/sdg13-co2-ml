# detector.py

from ultralytics import YOLO
from PIL import Image
import numpy as np
from config import YOLO_TO_APPLIANCE

model = YOLO("yolov8n.pt")


def detect_appliances(image: Image.Image) -> dict:
    """
    Detects appliances from a single PIL image.
    Returns dict: {"tv": 1, "fan": 2}
    """
    img_array = np.array(image)
    results = model(img_array, verbose=False)

    detected = {}

    for result in results:
        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])

            if confidence < 0.35:
                continue

            if class_name in YOLO_TO_APPLIANCE:
                key = YOLO_TO_APPLIANCE[class_name]
                detected[key] = detected.get(key, 0) + 1

    return detected


def detect_from_multiple(images: list) -> dict:
    """
    Detects from multiple photos of same room.
    Returns MAX count seen across all photos.
    """
    combined = {}

    for image in images:
        result = detect_appliances(image)
        for appliance, count in result.items():
            combined[appliance] = max(
                combined.get(appliance, 0), count
            )

    return combined
